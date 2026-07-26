"""Binary-split intuition, decision trees, and random forests for xG, mirroring
course22 nb07: hand-rolled single-split scoring first, then sklearn models, ending in
the feature-importance plot."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
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


def evaluate(model, xs, y):
    """{'log_loss', 'auc', 'xg_sum', 'goals'} — proper-scoring metrics; accuracy is
    useless at a ~6% goal base rate."""
    p = model.predict_proba(xs)[:, 1]
    return {"log_loss": log_loss(y, p), "auc": roc_auc_score(y, p),
            "xg_sum": p.sum(), "goals": int(y.sum())}


def plot_importance(model, cols, top=30):
    """Horizontal-bar feature importance plot from a fitted tree/forest."""
    imp = pd.Series(model.feature_importances_, index=cols).sort_values()
    imp[-top:].plot(kind="barh", figsize=(8, max(4, top * 0.28)))
    plt.title("Feature importance")
    plt.tight_layout()
    return imp.sort_values(ascending=False)
