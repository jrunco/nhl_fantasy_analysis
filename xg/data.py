"""Shot-level dataset access for xG modeling. Reads only games already cached in
nhl.game_pbp_raw, so loads are instant, reproducible, and make zero live API calls."""

from sklearn.model_selection import train_test_split
from sqlalchemy import text

from utils.function_library import build_shot_dataframe, _pg_engine


def cached_game_numbers(season="20232024", game_type="02"):
    """Sorted 1-based game numbers already cached in postgres for `season`."""
    lo = int(f"{season[:4]}{game_type}0000")
    with _pg_engine().connect() as conn:
        rows = conn.execute(
            text("SELECT game_id FROM nhl.game_pbp_raw WHERE game_id BETWEEN :lo AND :hi ORDER BY game_id"),
            {"lo": lo, "hi": lo + 9999},
        ).fetchall()
    return [r[0] % 10000 for r in rows]


def load_cached_shots(season="20232024", game_type="02"):
    """One row per unblocked shot across every cached game of `season`."""
    nums = cached_game_numbers(season, game_type)
    if not nums:
        raise RuntimeError(f"no cached games for {season}: pull some with build_shot_dataframe first")
    return build_shot_dataframe(season, game_numbers=nums, game_type=game_type)


def split_by_game(df, valid_frac=0.25, seed=42):
    """Train/valid split on whole games rather than rows, so rebound chains and other
    within-game sequences never straddle the split. Returns (trn_df, val_df)."""
    games = df["game_id"].unique()
    trn_g, val_g = train_test_split(games, test_size=valid_frac, random_state=seed)
    trn = df[df["game_id"].isin(trn_g)].reset_index(drop=True)
    val = df[df["game_id"].isin(val_g)].reset_index(drop=True)
    return trn, val
