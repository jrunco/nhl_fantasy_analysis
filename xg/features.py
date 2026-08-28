"""Feature engineering for the xG model, mirroring course22 nb05: fill missing values
with column modes, log-transform long-tailed continuous columns, one-hot categoricals,
normalize to [0,1] by column max. Nothing predictive is excluded at this stage — the
only drops are the label itself, columns that leak it (event_type IS the label), exact
string duplicates of id/numeric columns, and the constant season column."""

import numpy as np
import pandas as pd
import torch

TARGET = "is_goal"
NET_HALF_WIDTH = 3.0  # goal mouth is 6 ft wide, posts at y = +/-3
LEAKY = ["event_type"]  # 'goal' vs 'shot-on-goal'/'missed-shot' encodes the outcome
DUPES = ["shooter_name", "goalie_name", "time_in_period", "season"]
CATS = ["home_team", "away_team", "shooting_team", "opponent_team", "venue",
        "venue_location", "zone_code", "shot_type", "strength_state", "situation_code",
        "prev_event_type", "prev_event_zone", "shooter_id", "goalie_id", "period"]
LOGGED = ["seconds_since_prev"]  # heavy right tail; see notebook histogram


def model_frame(shots):
    """Raw shot rows -> modeling frame: drop leak/dupes, game_date -> day-of-season
    ordinal, add goal-mouth geometry, categoricals cast to pandas Categorical. Keeps every
    other column."""
    df = shots.drop(columns=[c for c in LEAKY + DUPES if c in shots]).copy()
    dates = pd.to_datetime(df["game_date"])
    df["day_of_season"] = (dates - dates.min()).dt.days
    df = df.drop(columns=["game_date"])
    df = add_geometry(df)
    for c in CATS:
        df[c] = pd.Categorical(df[c])
    return df


def add_geometry(df):
    """Add `aperture`: the angular width (radians) of the goal mouth as seen from the shot,
    signed by which side of the goal-line plane the shooter is on.

        aperture = 2*arctan(3/distance) * cos(angle)

    `shot_distance` alone can't express "behind the net" — it is built from hypot(), which
    discards the sign of the goal-line offset, so a shot 6 ft *behind* the net and a 6 ft
    tap-in from the slot are the same number. `shot_angle` keeps the sign (atan2 against a
    negative offset puts behind-the-line shots above 90 deg), so cos(angle) recovers it:
    +1 straight on, exactly 0 on the goal line extended (edge-on: no target at all), -1
    directly behind. Combining the two gives one scalar that is monotone in P(goal) and
    goes negative exactly where a direct shot becomes impossible.

    Distance is floored at 0.5 ft so shots recorded on the goal crease don't blow up."""
    d = df["shot_distance"].clip(lower=0.5)
    df = df.copy()
    df["aperture"] = 2 * np.arctan(NET_HALF_WIDTH / d) * np.cos(np.radians(df["shot_angle"]))
    return df


def fill_missing(df, modes=None):
    """Mode-fill NAs (nb05's `df.fillna(modes)`). Pass train-set modes when filling
    the validation set. Returns (filled_df, modes)."""
    if modes is None:
        modes = df.mode().iloc[0]
    return df.fillna(modes), modes


def add_log_cols(df):
    """log1p versions of the LOGGED long-tailed columns, alongside the originals."""
    df = df.copy()
    for c in LOGGED:
        df[f"log_{c}"] = np.log1p(df[c].astype(float))
    return df


def tree_frame(df):
    """nb07-style frame for sklearn trees: categoricals as integer codes (trees split
    on thresholds, so codes are fine even for high-cardinality ids)."""
    out = df.copy()
    for c in CATS:
        out[c] = out[c].cat.codes
    return out


def dummy_frame(df, max_levels=50):
    """nb05-style frame for the linear/NN models: one-hot categoricals. Columns with
    more than `max_levels` levels (shooter/goalie ids) become integer codes instead of
    exploding into hundreds of dummies."""
    out = df.copy()
    wide = [c for c in CATS if len(out[c].cat.categories) > max_levels]
    for c in wide:
        out[c] = out[c].cat.codes
    return pd.get_dummies(out, columns=[c for c in CATS if c not in wide])


def xs_y(df, dep=TARGET):
    """(features_df, target_series); features are everything but the target."""
    return df.drop(columns=[dep]), df[dep]


def to_tensors(df, dep=TARGET, maxes=None):
    """Float tensors for gradient descent, normalized column-wise to [0,1] by max
    (nb05's `t_indep / vals`). Pass train-set `maxes` for the validation set.
    Returns (t_indep, t_dep, col_names, maxes)."""
    xs, y = xs_y(df, dep)
    t_indep = torch.tensor(xs.to_numpy(dtype=np.float32))
    t_dep = torch.tensor(y.to_numpy(dtype=np.float32))
    if maxes is None:
        maxes = t_indep.max(dim=0).values
        maxes[maxes == 0] = 1.0
    return t_indep / maxes, t_dep, list(xs.columns), maxes
