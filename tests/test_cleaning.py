"""Tests of the cleaning functions in `src/cleaning.py` (board #27).

Run from the repository root with `pytest`.
Each test builds a tiny DataFrame by hand, so it shows one behaviour and runs fast.
The last tests run the whole chain on the real CSVs in `docs/raw data/`.
"""
from pathlib import Path

import pandas as pd
import pytest

from src.cleaning import (
    add_has_female_team,
    add_is_sexualized,
    add_region,
    add_role_tier,
    add_share_sexualized,
    add_share_women,
    add_team_group,
    clean_all,
    drop_age,
    drop_empty_games_columns,
    drop_review_sites,
    drop_unused_games_columns,
    fill_series,
    fix_percentages,
    fix_release_date,
    fix_son_damsel_flag,
    read_raw_tables,
    rename_columns,
    validate_tables,
)

RAW_DIR = Path(__file__).resolve().parent.parent / "docs" / "raw data"


# ----------------------------------------------------------------------------- dropping columns
def test_drop_empty_games_columns_removes_unnamed_27():
    games = pd.DataFrame({"Title": ["A"], "Unnamed: 27": [None]})
    assert drop_empty_games_columns(games).columns.tolist() == ["Title"]


def test_drop_empty_games_columns_works_when_column_is_already_gone():
    games = pd.DataFrame({"Title": ["A"]})
    assert drop_empty_games_columns(games).columns.tolist() == ["Title"]


def test_drop_unused_games_columns_keeps_the_others():
    games = pd.DataFrame(columns=["Title", "Sub-genre", "Publisher", "Platform", "PEGI", "Criteria"])
    assert drop_unused_games_columns(games).columns.tolist() == ["Title"]


def test_drop_age_keeps_age_range():
    characters = pd.DataFrame({"Age": ["Adult"], "Age_range": ["Adult"]})
    assert drop_age(characters).columns.tolist() == ["Age_range"]


def test_drop_review_sites_keeps_avg_reviews_and_handles_trailing_space():
    games = pd.DataFrame(columns=["Metacritic ", "Destructoid", "IGN", "GameSpot", "Avg_Reviews"])
    assert drop_review_sites(games).columns.tolist() == ["Avg_Reviews"]


# ----------------------------------------------------------------------------- fill and rename
def test_fill_series_labels_missing_as_standalone():
    games = pd.DataFrame({"Series": ["Zelda", None]})
    result = fill_series(games)
    assert result["Series"].tolist() == ["Zelda", "Standalone"]
    assert games["Series"].isna().sum() == 1      # the input is untouched


def test_rename_columns_renames_only_the_known_columns():
    tables = {
        "games": pd.DataFrame(columns=["female_team", "Title"]),
        "characters": pd.DataFrame(columns=["Name"]),
        "sexualization": pd.DataFrame(columns=["Damsel in Distress", "Sexualized Cutscenes", "Trophy"]),
    }
    renamed = rename_columns(tables)
    assert renamed["games"].columns.tolist() == ["Female_team", "Title"]
    assert renamed["characters"].columns.tolist() == ["Name"]
    assert renamed["sexualization"].columns.tolist() == ["Damsel_in_distress", "Sexualized_cutscenes", "Trophy"]
    assert tables["games"].columns.tolist() == ["female_team", "Title"]      # the input dict is untouched


# ----------------------------------------------------------------------------- types
def test_fix_release_date_gives_a_date_and_a_year():
    games = pd.DataFrame({"Release": ["Nov-13", "Jan-22"]})
    result = fix_release_date(games)
    assert result["Release"].tolist() == [pd.Timestamp("2013-11-01"), pd.Timestamp("2022-01-01")]
    assert result["Release_year"].tolist() == [2013, 2022]


def test_fix_percentages_turns_text_into_floats():
    games = pd.DataFrame({"Percentage_non_male": ["50%", "27.8%"], "Team_percentage": ["0%", "14.75%"]})
    result = fix_percentages(games)
    assert result["Percentage_non_male"].tolist() == [50.0, 27.8]
    assert result["Team_percentage"].tolist() == [0.0, 14.75]


# ----------------------------------------------------------------------------- the Son correction
def _sexualization_with_son():
    return pd.DataFrame({
        "Id": ["PP_Son", "PP_Mum"],
        "Sexualized_clothing": [0, 1],
        "Trophy": [0, 0],
        "Damsel_in_distress": [1, 0],
        "Sexualized_cutscenes": [0, 0],
        "Total": [1, 1],
    })


def _characters_with_son():
    return pd.DataFrame({"Id": ["PP_Son", "PP_Mum"], "Sexualization": [1, 1]})


def test_fix_son_damsel_flag_corrects_son_and_recomputes_scores():
    sexualization, characters = fix_son_damsel_flag(_sexualization_with_son(), _characters_with_son())
    son = sexualization.set_index("Id").loc["PP_Son"]
    assert son["Damsel_in_distress"] == 0
    assert son["Total"] == 0
    assert characters.set_index("Id").loc["PP_Son", "Sexualization"] == 0


def test_fix_son_damsel_flag_leaves_other_characters_unchanged():
    sexualization, characters = fix_son_damsel_flag(_sexualization_with_son(), _characters_with_son())
    assert sexualization.set_index("Id").loc["PP_Mum", "Total"] == 1
    assert characters.set_index("Id").loc["PP_Mum", "Sexualization"] == 1


def test_fix_son_damsel_flag_does_not_modify_its_inputs():
    sexualization, characters = _sexualization_with_son(), _characters_with_son()
    fix_son_damsel_flag(sexualization, characters)
    assert sexualization.loc[0, "Damsel_in_distress"] == 1
    assert characters.loc[0, "Sexualization"] == 1


# ----------------------------------------------------------------------------- features (characters)
def test_add_is_sexualized_is_true_only_above_zero():
    characters = pd.DataFrame({"Sexualization": [0, 1, 3]})
    assert add_is_sexualized(characters)["Is_sexualized"].tolist() == [False, True, True]


def test_add_role_tier_groups_relevance_in_three_ordered_levels():
    characters = pd.DataFrame({"Relevance": ["PA", "DA", "MC", "MA", "SK", "SC"]})
    tier = add_role_tier(characters)["Role_tier"]
    assert tier.astype(str).tolist() == ["Lead", "Major", "Major", "Major", "Minor", "Minor"]
    assert tier.cat.ordered
    assert tier.cat.categories.tolist() == ["Lead", "Major", "Minor"]


# ----------------------------------------------------------------------------- features (games)
def test_add_has_female_team_is_true_only_above_zero():
    games = pd.DataFrame({"Team_percentage": [0.0, 0.5, 40.0]})
    assert add_has_female_team(games)["Has_female_team"].tolist() == [False, True, True]


def test_add_team_group_boundaries():
    games = pd.DataFrame({"Team_percentage": [0.0, 1.0, 25.0, 26.0]})
    groups = add_team_group(games)["Team_group"].astype(str).tolist()
    assert groups == ["0%", "1-25%", "1-25%", ">25%"]


def test_add_share_women_is_a_percentage_of_the_games_characters():
    games = pd.DataFrame({"Game_Id": ["G1", "G2"]})
    characters = pd.DataFrame({
        "Game": ["G1", "G1", "G1", "G1", "G2"],
        "Gender": ["Female", "Male", "Male", "Non-binary", "Female"],
    })
    shares = add_share_women(games, characters)["Share_women"].tolist()
    assert shares == [25.0, 100.0]       # Non-binary stays in the denominator


def test_add_share_sexualized_is_a_percentage_of_the_games_characters():
    games = pd.DataFrame({"Game_Id": ["G1", "G2"]})
    characters = pd.DataFrame({
        "Game": ["G1", "G1", "G2"],
        "Is_sexualized": [True, False, False],
    })
    shares = add_share_sexualized(games, characters)["Share_sexualized"].tolist()
    assert shares == [50.0, 0.0]


def test_add_region_groups_small_countries_in_rest_of_world():
    games = pd.DataFrame({"Country": ["USA", "JPN", "CAN", "GBR", "AUS"]})
    regions = add_region(games)["Region"].tolist()
    assert regions == ["USA", "Japan", "Canada", "Rest of world", "Rest of world"]


# ----------------------------------------------------------------------------- validate_tables
def _valid_tables():
    return {
        "characters": pd.DataFrame({"Id": ["A_1", "A_2"], "Sexualization": [0, 2]}),
        "sexualization": pd.DataFrame({
            "Id": ["A_1", "A_2"],
            "Sexualized_clothing": [0, 1],
            "Trophy": [0, 0],
            "Damsel_in_distress": [0, 1],
            "Sexualized_cutscenes": [0, 0],
            "Total": [0, 2],
        }),
    }


def test_validate_tables_finds_no_problem_in_consistent_tables():
    assert validate_tables(_valid_tables()) == []


def test_validate_tables_reports_a_criterion_that_is_not_0_or_1():
    tables = _valid_tables()
    tables["sexualization"].loc[0, "Trophy"] = 2
    assert any("0 or 1" in p for p in validate_tables(tables))


def test_validate_tables_reports_a_total_that_is_not_the_sum_of_the_criteria():
    tables = _valid_tables()
    tables["sexualization"].loc[1, "Total"] = 1
    assert any("Total" in p for p in validate_tables(tables))


def test_validate_tables_reports_ids_missing_in_one_table():
    tables = _valid_tables()
    tables["sexualization"] = tables["sexualization"].iloc[:1]
    assert any("Id" in p for p in validate_tables(tables))


def test_validate_tables_reports_a_sexualization_that_differs_from_total():
    tables = _valid_tables()
    tables["characters"].loc[1, "Sexualization"] = 1
    assert any("Sexualization" in p for p in validate_tables(tables))


# ----------------------------------------------------------------------------- the whole chain, real data
@pytest.fixture(scope="module")
def raw_tables():
    return read_raw_tables(RAW_DIR)


@pytest.fixture(scope="module")
def clean_tables(raw_tables):
    return clean_all(raw_tables)


def test_read_raw_tables_has_the_expected_shapes(raw_tables):
    assert raw_tables["games"].shape == (64, 28)
    assert raw_tables["characters"].shape == (637, 12)
    assert raw_tables["sexualization"].shape == (637, 6)


def test_clean_all_does_not_modify_the_raw_tables(raw_tables):
    before = {name: d.copy() for name, d in raw_tables.items()}
    clean_all(raw_tables)
    for name, d in raw_tables.items():
        pd.testing.assert_frame_equal(d, before[name])


def test_clean_all_keeps_every_row(clean_tables):
    assert len(clean_tables["games"]) == 64
    assert len(clean_tables["characters"]) == 637
    assert len(clean_tables["sexualization"]) == 637


def test_clean_all_drops_the_columns_we_decided_to_drop(clean_tables):
    games, characters = clean_tables["games"], clean_tables["characters"]
    for column in ["Unnamed: 27", "Sub-genre", "Publisher", "Platform", "PEGI", "Criteria",
                   "Metacritic ", "Destructoid", "IGN", "GameSpot"]:
        assert column not in games.columns
    assert "Age" not in characters.columns


def test_clean_all_has_no_missing_series_and_the_expected_standalone_count(clean_tables):
    series = clean_tables["games"]["Series"]
    assert series.isna().sum() == 0
    assert (series == "Standalone").sum() == 37


def test_clean_all_numeric_columns_are_numbers(clean_tables):
    games = clean_tables["games"]
    assert pd.api.types.is_float_dtype(games["Team_percentage"])
    assert pd.api.types.is_datetime64_any_dtype(games["Release"])
    assert games["Release_year"].between(2012, 2022).all()


def test_clean_all_gives_the_numbers_quoted_in_the_notebook(clean_tables):
    games, characters = clean_tables["games"], clean_tables["characters"]
    assert characters["Is_sexualized"].sum() == 34
    assert games["Team_group"].astype(str).value_counts().to_dict() == {"0%": 36, "1-25%": 20, ">25%": 8}
    men = characters[characters["Gender"] == "Male"]
    women = characters[characters["Gender"] == "Female"]
    assert (len(women), women["Is_sexualized"].sum()) == (203, 29)
    assert (len(men), men["Is_sexualized"].sum()) == (393, 4)      # 4, not 5: the Son row is corrected


def test_clean_all_gives_tables_that_pass_validation(clean_tables):
    assert validate_tables(clean_tables) == []
