"""Reusable cleaning and feature-engineering functions (board #24).

Each function takes DataFrames, returns new ones and never changes its input.
The notebook calls them one step at a time (each step sits next to its
"Decision / Why" text); `clean_all` runs the whole chain in one call and is
what the dashboard (`app.py`) uses.

Tables: `games` (one row per game), `characters` (one row per character),
`sexualization` (one row per character, same `Id`).
"""
from pathlib import Path

import pandas as pd

RAW_FILES = {
    "games": "games.grivg.csv",
    "characters": "characters.grivg.csv",
    "sexualization": "sexualization.grivg.csv",
}

# Columns dropped on purpose, see the Limpieza section of the notebook.
EMPTY_GAMES_COLUMNS = ["Unnamed: 27"]
UNUSED_GAMES_COLUMNS = ["Sub-genre", "Publisher", "Platform", "PEGI", "Criteria"]
REVIEW_SITE_COLUMNS = ["Metacritic ", "Destructoid", "IGN", "GameSpot"]   # "Metacritic " has a trailing space

RENAME_MAP = {
    "games": {"female_team": "Female_team"},
    "sexualization": {
        "Damsel in Distress": "Damsel_in_distress",
        "Sexualized Cutscenes": "Sexualized_cutscenes",
    },
}

SEXUALIZATION_CRITERIA = ["Sexualized_clothing", "Trophy", "Damsel_in_distress", "Sexualized_cutscenes"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PERCENT_COLUMNS = ["Percentage_non_male", "Team_percentage"]

ROLE_TIERS = {"PA": "Lead", "DA": "Major", "MC": "Major", "MA": "Major", "SK": "Minor", "SC": "Minor"}
TIER_ORDER = ["Lead", "Major", "Minor"]
TEAM_GROUP_BINS = [-1, 0, 25, 100]            # -1 so that exactly 0% gets its own group
TEAM_GROUP_LABELS = ["0%", "1-25%", ">25%"]
REGION_MAP = {"USA": "USA", "JPN": "Japan", "CAN": "Canada"}
OTHER_REGION = "Rest of world"                # Europe + Australia

SON_ID = "PP_Son"                             # a Child flagged as "damsel in distress" (data error)


# ----------------------------------------------------------------------------- loading
def read_raw_tables(directory: Path | str) -> dict[str, pd.DataFrame]:
    """Read the three raw CSV files of the dataset from `directory`."""
    directory = Path(directory)
    return {name: pd.read_csv(directory / file, encoding="utf-8-sig") for name, file in RAW_FILES.items()}


# ----------------------------------------------------------------------------- cleaning
def drop_empty_games_columns(games: pd.DataFrame) -> pd.DataFrame:
    """Drop the empty column `Unnamed: 27` (a trailing comma in the CSV)."""
    return games.drop(columns=EMPTY_GAMES_COLUMNS, errors="ignore")


def drop_unused_games_columns(games: pd.DataFrame) -> pd.DataFrame:
    """Drop the games columns the three questions do not use."""
    return games.drop(columns=UNUSED_GAMES_COLUMNS)


def drop_age(characters: pd.DataFrame) -> pd.DataFrame:
    """Drop `Age`: its words equal `Age_range` and its numbers fall in the right range."""
    return characters.drop(columns=["Age"])


def drop_review_sites(games: pd.DataFrame) -> pd.DataFrame:
    """Keep only `Avg_Reviews` and drop the four individual review-site scores."""
    return games.drop(columns=REVIEW_SITE_COLUMNS)


def fill_series(games: pd.DataFrame) -> pd.DataFrame:
    """A missing `Series` means the game belongs to no series: label it `"Standalone"`."""
    games = games.copy()
    games["Series"] = games["Series"].fillna("Standalone")
    return games


def rename_columns(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Give the columns `Capitalized_with_underscores` names. Returns a new dict."""
    return {name: d.rename(columns=RENAME_MAP.get(name, {})) for name, d in tables.items()}


def fix_release_date(games: pd.DataFrame) -> pd.DataFrame:
    """Turn `Release` ("Nov-13") into a date (first of the month) and add `Release_year`."""
    games = games.copy()
    month = games["Release"].str[:3].map({m: i for i, m in enumerate(MONTHS, start=1)})
    year = 2000 + games["Release"].str[-2:].astype(int)       # "13" -> 2013 (games are 2012-2022)
    games["Release"] = pd.to_datetime(pd.DataFrame({"year": year, "month": month, "day": 1}))
    games["Release_year"] = games["Release"].dt.year
    return games


def fix_percentages(games: pd.DataFrame) -> pd.DataFrame:
    """Turn the text percentages ("14.5%") into floats."""
    games = games.copy()
    for col in PERCENT_COLUMNS:
        games[col] = games[col].astype(str).str.rstrip("%").astype(float)
    return games


def fix_son_damsel_flag(
    sexualization: pd.DataFrame, characters: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Correct the `PP_Son` row, recompute `Total` and copy it to `characters.Sexualization`.

    Returns (sexualization, characters).
    """
    sexualization = sexualization.copy()
    characters = characters.copy()
    sexualization.loc[sexualization["Id"] == SON_ID, "Damsel_in_distress"] = 0
    sexualization["Total"] = sexualization[SEXUALIZATION_CRITERIA].sum(axis=1)
    characters["Sexualization"] = characters["Id"].map(sexualization.set_index("Id")["Total"])
    return sexualization, characters


# ----------------------------------------------------------------------------- features
def add_is_sexualized(characters: pd.DataFrame) -> pd.DataFrame:
    """Add `Is_sexualized`: True when the sexualization score is above 0."""
    characters = characters.copy()
    characters["Is_sexualized"] = characters["Sexualization"] > 0
    return characters


def add_role_tier(characters: pd.DataFrame) -> pd.DataFrame:
    """Add the ordered `Role_tier` (Lead / Major / Minor) built from `Relevance`."""
    characters = characters.copy()
    characters["Role_tier"] = pd.Categorical(
        characters["Relevance"].map(ROLE_TIERS), categories=TIER_ORDER, ordered=True)
    return characters


def add_has_female_team(games: pd.DataFrame) -> pd.DataFrame:
    """Add `Has_female_team`: True when at least one woman is in the development team."""
    games = games.copy()
    games["Has_female_team"] = games["Team_percentage"] > 0
    return games


def add_team_group(games: pd.DataFrame) -> pd.DataFrame:
    """Add `Team_group` (0% / 1-25% / >25% women in the team)."""
    games = games.copy()
    games["Team_group"] = pd.cut(games["Team_percentage"], bins=TEAM_GROUP_BINS, labels=TEAM_GROUP_LABELS)
    return games


def add_share_women(games: pd.DataFrame, characters: pd.DataFrame) -> pd.DataFrame:
    """Add `Share_women`: percentage of a game's characters who are women (unit: the game)."""
    games = games.copy()
    share = (characters["Gender"] == "Female").groupby(characters["Game"]).mean() * 100
    games["Share_women"] = games["Game_Id"].map(share)
    return games


def add_share_sexualized(games: pd.DataFrame, characters: pd.DataFrame) -> pd.DataFrame:
    """Add `Share_sexualized`: percentage of a game's characters with a score above 0.

    `characters` must already have `Is_sexualized` (see `add_is_sexualized`).
    """
    games = games.copy()
    games["Share_sexualized"] = games["Game_Id"].map(characters.groupby("Game")["Is_sexualized"].mean() * 100)
    return games


def add_region(games: pd.DataFrame) -> pd.DataFrame:
    """Add `Region`: USA / Japan / Canada / Rest of world, grouped from `Country`."""
    games = games.copy()
    games["Region"] = games["Country"].map(REGION_MAP).fillna(OTHER_REGION)
    return games


# ----------------------------------------------------------------------------- the whole chain
def clean_all(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Run every cleaning and feature step in the notebook's order.

    `raw` is the dict of the three raw tables (see `read_raw_tables`).
    Returns a new dict with the cleaned `games`, `characters` and `sexualization`.
    """
    games = drop_empty_games_columns(raw["games"])
    games = drop_unused_games_columns(games)
    characters = drop_age(raw["characters"])
    games = drop_review_sites(games)
    games = fill_series(games)
    tables = rename_columns({"games": games, "characters": characters, "sexualization": raw["sexualization"]})
    games = fix_percentages(fix_release_date(tables["games"]))
    sexualization, characters = fix_son_damsel_flag(tables["sexualization"], tables["characters"])
    characters = add_role_tier(add_is_sexualized(characters))
    games = add_has_female_team(games)
    games = add_team_group(games)
    games = add_share_women(games, characters)
    games = add_share_sexualized(games, characters)
    games = add_region(games)
    return {"games": games, "characters": characters, "sexualization": sexualization}
