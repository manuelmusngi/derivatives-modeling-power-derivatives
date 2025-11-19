import polars as pl
from pathlib import Path

def read_spot(path: str, date_col: str, spot_col: str) -> pl.DataFrame:
    return (pl.read_csv(path, try_parse_dates=True)
              .rename({date_col: "date", spot_col: "spot"})
              .with_columns(pl.col("date").cast(pl.Date))
              .sort("date"))

def read_forwards(path: str, date_col: str, forward_cols: list[str]) -> pl.DataFrame:
    df = pl.read_csv(path, try_parse_dates=True).rename({date_col: "date"})
    df = df.with_columns(pl.col("date").cast(pl.Date)).sort("date")
    # forward columns remain as-is; ensure numeric
    return df.select(["date"] + forward_cols)

def write_df(df: pl.DataFrame, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(path)
