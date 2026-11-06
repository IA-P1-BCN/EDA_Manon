"""Tests of `pipeline.py` (board #26): the whole chain from raw CSVs to clean CSVs.

Run from the repository root with `pytest`. Files are written to pytest's temporary folder,
never to `data/clean/`.
"""
import shutil
from pathlib import Path

import pandas as pd

import pipeline
from src.cleaning import clean_all, read_raw_tables

RAW_DIR = Path(__file__).resolve().parent.parent / "docs" / "raw data"


def test_run_saves_the_three_clean_tables(tmp_path):
    tables = pipeline.run(RAW_DIR, tmp_path)
    for name, table in tables.items():
        saved = pd.read_csv(tmp_path / f"{name}.csv")
        assert saved.shape == table.shape


def test_run_gives_the_same_tables_as_clean_all(tmp_path):
    from_pipeline = pipeline.run(RAW_DIR, tmp_path)
    direct = clean_all(read_raw_tables(RAW_DIR))
    for name in direct:
        pd.testing.assert_frame_equal(from_pipeline[name], direct[name])


def test_run_twice_gives_identical_files(tmp_path):
    pipeline.run(RAW_DIR, tmp_path / "first")
    pipeline.run(RAW_DIR, tmp_path / "second")
    for name in ["games", "characters", "sexualization"]:
        assert (tmp_path / "first" / f"{name}.csv").read_bytes() == (tmp_path / "second" / f"{name}.csv").read_bytes()


def test_main_stops_and_saves_nothing_when_the_data_is_inconsistent(tmp_path, capsys):
    broken_raw = tmp_path / "raw"
    shutil.copytree(RAW_DIR, broken_raw)
    sexualization_file = broken_raw / "sexualization.grivg.csv"
    sexualization = pd.read_csv(sexualization_file, encoding="utf-8-sig")
    sexualization.loc[0, "Trophy"] = 5                      # a criterion must be 0 or 1
    sexualization.to_csv(sexualization_file, index=False)

    exit_code = pipeline.main(["--raw", str(broken_raw), "--out", str(tmp_path / "out")])

    assert exit_code == 1
    assert not (tmp_path / "out").exists()
    assert "nothing saved" in capsys.readouterr().err
