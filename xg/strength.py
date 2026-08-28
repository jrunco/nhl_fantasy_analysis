"""Strength-state stratification for xG.

Evolving Hockey trains four separate models — even strength, powerplay, shorthanded,
empty net — rather than one pooled model, and their published AUCs differ sharply by
state (EV 0.782, PP 0.718, SH 0.798). A single pooled model has to average those regimes
into one function, so the shot-quality geometry of a 5v4 (open lanes, set formation) gets
smeared together with 5v5. This module labels shots, fits one model per bucket, and
scores that against the pooled baseline on identical validation rows.

Any `fit_fn(xs, y)` works — `trees.fit_gbm`, `trees.fit_forest`, `trees.fit_tree`."""

import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, roc_auc_score

from xg.features import TARGET, xs_y

BUCKETS = ("EV", "PP", "SH", "EN")
MIN_ROWS = 500        # a bucket thinner than this can't support its own model
MIN_GOALS = 20        # ...nor one with too few positives to shape a probability
POOLED = "_pooled"


def strength_bucket(df):
    """EV/PP/SH/EN label per shot, as a Series aligned to `df.index`.

    Empty net outranks man-advantage: `is_empty_net` means the *opponent's* goalie is
    pulled, so a 5v6 shot at an empty net is EN, not SH. Shots where the shooter's own
    team pulled its goalie (6v5, still facing a goalie) land in PP — skater differential
    is what drives shot quality, and that matches Evolving Hockey's four-way split."""
    for c in ("is_empty_net", "shooter_skaters", "opponent_skaters"):
        if c not in df:
            raise KeyError(f"strength_bucket needs '{c}'; build the frame with features.model_frame")
    diff = df["shooter_skaters"] - df["opponent_skaters"]
    lab = np.where(diff > 0, "PP", np.where(diff < 0, "SH", "EV"))
    en = df["is_empty_net"].fillna(0).astype(int) == 1
    return pd.Series(np.where(en, "EN", lab), index=df.index, name="strength_bucket")


def bucket_counts(df, dep=TARGET):
    """Shots / goals / goal rate per bucket — check this before trusting a split, since
    SH and EN are thin at any sample size short of several full seasons."""
    b = strength_bucket(df)
    out = df.groupby(b, observed=True)[dep].agg(shots="size", goals="sum")
    out["goal_rate"] = (out.goals / out.shots).round(4)
    return out.reindex([x for x in BUCKETS if x in out.index])


def fit_by_strength(trn, fit_fn, min_rows=MIN_ROWS, min_goals=MIN_GOALS, dep=TARGET):
    """{bucket: model}, plus a POOLED model trained on every shot. Buckets thinner than
    `min_rows`/`min_goals` get no model of their own and fall back to POOLED at predict
    time — a 60-shot EN model is worse than no EN model."""
    xs, y = xs_y(trn, dep)
    b = strength_bucket(trn)
    models = {POOLED: fit_fn(xs, y)}
    for name in BUCKETS:
        m = (b == name).to_numpy()
        if m.sum() < min_rows or not min_goals <= y[m].sum() < m.sum():
            continue
        models[name] = fit_fn(xs[m], y[m])
    return models


def predict_by_strength(models, df, dep=TARGET):
    """P(goal) for every row of `df`, each routed to its bucket model (POOLED where that
    bucket has none). Returns a Series aligned to `df.index`."""
    xs, _ = xs_y(df, dep)
    b = strength_bucket(df)
    out = pd.Series(np.nan, index=df.index, dtype=float)
    for name in b.unique():
        m = (b == name).to_numpy()
        out[m] = models.get(name, models[POOLED]).predict_proba(xs[m])[:, 1]
    if out.isna().any():
        raise RuntimeError(f"{int(out.isna().sum())} rows left unpredicted")
    return out


def compare(trn, val, fit_fn, min_rows=MIN_ROWS, min_goals=MIN_GOALS, dep=TARGET):
    """Pooled vs per-bucket on identical validation rows. Returns (models, table), where
    the table is indexed by bucket plus 'ALL' and carries shots/goals and log loss, AUC,
    Σ xG for each approach. 'ALL' is the number that decides whether splitting paid off;
    the per-bucket rows say where it came from."""
    models = fit_by_strength(trn, fit_fn, min_rows, min_goals, dep)
    xs, y = xs_y(val, dep)
    pooled = pd.Series(models[POOLED].predict_proba(xs)[:, 1], index=val.index)
    split = predict_by_strength(models, val, dep)

    b = strength_bucket(val)
    rows = {}
    for name in [x for x in BUCKETS if (b == x).any()] + ["ALL"]:
        m = (b == name).to_numpy() if name != "ALL" else np.ones(len(val), bool)
        rows[name] = {"shots": int(m.sum()), "goals": int(y[m].sum()),
                      "own_model": name in models,
                      **_scores(y[m], pooled[m], "pooled"),
                      **_scores(y[m], split[m], "split")}
    return models, pd.DataFrame(rows).T


# ------------------------------------------------------------------------------------- #
# helpers
# ------------------------------------------------------------------------------------- #

def _scores(y, p, tag):
    """{'<tag>_log_loss', '<tag>_auc', '<tag>_xg'}; AUC is NaN when the slice is
    single-class (thin EN samples are often all goals)."""
    auc = roc_auc_score(y, p) if y.nunique() > 1 else np.nan
    return {f"{tag}_log_loss": log_loss(y, p, labels=[0, 1]), f"{tag}_auc": auc,
            f"{tag}_xg": round(float(p.sum()), 1)}
