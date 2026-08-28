"""Binary-split intuition, decision trees, random forests, and gradient boosting for xG,
mirroring course22 nb07: hand-rolled single-split scoring first, then sklearn models,
ending in the feature-importance plot."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.tree import DecisionTreeClassifier


def side_score(side, y):
    """Impurity contribution of one side of a split: std of the target within the
    side, weighted by its size (nb07's `_side_score`)."""
    tot = side.sum()
    if tot <= 1:
        return 0
    return y[side].std() * tot


def split_score(col, y, split):
    """Weighted-std score of splitting `col` at <= `split`; lower is better."""
    lhs = col <= split
    return (side_score(lhs, y) + side_score(~lhs, y)) / len(y)


def best_split(df, col, dep):
    """Best single threshold for `col` by exhaustive scan of its unique values.
    Returns (threshold, score)."""
    c, y = df[col], df[dep]
    unq = c.dropna().unique()
    scores = np.array([split_score(c, y, o) for o in unq if not np.isnan(o)])
    idx = scores.argmin()
    return unq[idx], scores[idx]


def all_best_splits(df, cols, dep):
    """{col: (threshold, score)} for each candidate column, sorted best-first."""
    res = {o: best_split(df, o, dep) for o in cols}
    return dict(sorted(res.items(), key=lambda kv: kv[1][1]))


def fit_tree(xs, y, **kwargs):
    kwargs.setdefault("min_samples_leaf", 50)
    return DecisionTreeClassifier(random_state=42, **kwargs).fit(xs, y)


def fit_forest(xs, y, n_estimators=200, **kwargs):
    kwargs.setdefault("min_samples_leaf", 10)
    kwargs.setdefault("max_features", 0.5)
    return RandomForestClassifier(n_estimators=n_estimators, random_state=42,
                                  oob_score=True, n_jobs=-1, **kwargs).fit(xs, y)


def fit_gbm(xs, y, **kwargs):
    """Histogram gradient boosting — descent in *function* space: each tree is fit to the
    negative gradient of log loss w.r.t. the current predictions, `learning_rate` is the
    step size. This is the algorithm MoneyPuck and Evolving Hockey actually use, so it is
    the like-for-like comparison against their published AUC/log loss.

    Unlike the forest it needs no imputation (NaN gets a learned default branch) and is
    invariant to monotone transforms, so the log/normalize steps in `features` are no-ops
    here. Early stopping picks the tree count, so `max_iter` is a ceiling, not a target."""
    kwargs.setdefault("max_iter", 500)
    kwargs.setdefault("learning_rate", 0.05)
    kwargs.setdefault("max_leaf_nodes", 31)
    kwargs.setdefault("min_samples_leaf", 40)
    kwargs.setdefault("l2_regularization", 1.0)
    kwargs.setdefault("early_stopping", True)
    kwargs.setdefault("validation_fraction", 0.15)
    kwargs.setdefault("n_iter_no_change", 25)
    return HistGradientBoostingClassifier(random_state=42, **kwargs).fit(xs, y)


def monotone_cst(cols, increasing=(), decreasing=()):
    """`monotonic_cst` vector for `fit_gbm`: +1 increasing, -1 decreasing, 0 unconstrained.

    Use this to *impose* a relationship the sample is too thin to learn — the behind-the-net
    discount rests on ~14 goals, which is far too few to fit but is settled physics. A
    constraint costs no degrees of freedom."""
    inc, dec = set(increasing), set(decreasing)
    unknown = (inc | dec) - set(cols)
    if unknown:
        raise KeyError(f"not in columns: {sorted(unknown)}")
    return [1 if c in inc else -1 if c in dec else 0 for c in cols]


def evaluate(model, xs, y):
    """{'log_loss', 'auc', 'xg_sum', 'goals'} — proper-scoring metrics; accuracy is
    useless at a ~6% goal base rate."""
    p = model.predict_proba(xs)[:, 1]
    return {"log_loss": log_loss(y, p), "auc": roc_auc_score(y, p),
            "xg_sum": p.sum(), "goals": int(y.sum())}


def perm_importance(model, xs, y, n_repeats=5, scoring="neg_log_loss"):
    """Permutation importance as a Series, best-first. Needed for `fit_gbm`, which has no
    `feature_importances_`, and honest for the forest too: impurity importance is biased
    toward high-cardinality columns (which is why `shooter_id`/`event_id` rank high there).
    Units are log-loss degradation when the column is shuffled.

    Caveat: this understates correlated groups. x/y coords, distance and angle are all
    functions of the same two numbers, so permuting one lets the model recover it from the
    others. It measures replaceability, not use."""
    r = permutation_importance(model, xs, y, n_repeats=n_repeats, scoring=scoring,
                               random_state=42, n_jobs=-1)
    return pd.Series(r.importances_mean, index=list(xs.columns)).sort_values(ascending=False)


def plot_importance(imp, cols=None, top=30):
    """Horizontal-bar importance plot. `imp` is either a fitted tree/forest (pass `cols`)
    or a precomputed Series from `perm_importance`."""
    if not isinstance(imp, pd.Series):
        imp = pd.Series(imp.feature_importances_, index=cols)
    imp = imp.sort_values()
    imp[-top:].plot(kind="barh", figsize=(8, max(4, top * 0.28)))
    plt.title("Feature importance")
    plt.tight_layout()
    return imp.sort_values(ascending=False)
