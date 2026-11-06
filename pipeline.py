"""Reproducible pipeline (board #26): raw CSVs -> cleaning -> checks -> clean CSVs.

Run with one command from the repository root:

    python pipeline.py

Steps:
  1. find the raw CSVs (the local copy in `docs/raw data/`, otherwise download them with kagglehub);
  2. clean them with `src/cleaning.py` (the same functions as the notebook and the dashboard);
  3. check the cleaned data is consistent (`validate_tables`); stop without saving if it is not;
  4. save the three clean tables as CSV files in `data/clean/`.

Options:  --raw FOLDER   read the raw CSVs from FOLDER instead
          --out FOLDER   write the clean CSVs to FOLDER (default: data/clean)
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

from src.cleaning import clean_all, read_raw_tables, validate_tables

ROOT = Path(__file__).parent
LOCAL_RAW_DIR = ROOT / "docs" / "raw data"
DEFAULT_OUT_DIR = ROOT / "data" / "clean"
KAGGLE_DATASET = "br33sa/gender-representation-in-video-games"


def find_raw_dir() -> Path:
    """Local copy of the CSVs if present, otherwise download them with kagglehub."""
    if (LOCAL_RAW_DIR / "games.grivg.csv").exists():
        return LOCAL_RAW_DIR
    import kagglehub
    return Path(kagglehub.dataset_download(KAGGLE_DATASET))


def run(raw_dir: Path | str | None = None, out_dir: Path | str = DEFAULT_OUT_DIR) -> dict[str, pd.DataFrame]:
    """Load, clean, check and save. Returns the clean tables.

    Raises ValueError (and saves nothing) if the cleaned data fails `validate_tables`.
    """
    raw_dir = Path(raw_dir) if raw_dir else find_raw_dir()
    print(f"1/4 Reading the raw CSVs from {raw_dir}")
    raw = read_raw_tables(raw_dir)

    print("2/4 Cleaning")
    tables = clean_all(raw)

    print("3/4 Checking the clean data")
    problems = validate_tables(tables)
    if problems:
        raise ValueError("The clean data is not consistent: " + "; ".join(problems))

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"4/4 Saving to {out_dir}")
    for name, table in tables.items():
        table.to_csv(out_dir / f"{name}.csv", index=False)
        print(f"    {name}.csv: {table.shape[0]} rows, {table.shape[1]} columns")
    return tables


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Clean the video-game gender dataset and save it as CSV files.")
    parser.add_argument("--raw", help="folder with the raw CSV files (default: local copy, else kagglehub)")
    parser.add_argument("--out", default=str(DEFAULT_OUT_DIR), help="folder for the clean CSV files (default: data/clean)")
    args = parser.parse_args(argv)
    try:
        run(args.raw, args.out)
    except ValueError as error:
        print(f"Stopped, nothing saved. {error}", file=sys.stderr)
        return 1
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
