
import polars as pl
import numpy as np

def fractional_year(date_col: pl.Series) -> np.ndarray:
    # Converts date to fractional year t in [year, year+1)
    dates = date_col.to_list()
    return np.array([(d.timetuple().tm_yday - 1) / 365.0 for d in dates])

def add_sinusoidal_seasonality(df: pl.DataFrame, freq_per_year: int=1, include_weekly: bool=True) -> pl.DataFrame:
    t = fractional_year(df["date"])
    cols = {}
    for k in range(1, freq_per_year + 1):
        cols[f"cos_{k}"] = np.cos(2 * np.pi * k * t)
        cols[f"sin_{k}"] = np.sin(2 * np.pi * k * t)
    out = df.with_columns([pl.Series(name, vals) for name, vals in cols.items()])
    if include_weekly:
        dow = df["date"].dt.weekday()
        out = out.with_columns(pl.col("date").dt.weekday().alias("dow"))
        out = out.with_columns([pl.when(pl.col("dow") == i).then(1).otherwise(0).alias(f"dow_{i}") for i in range(7)])
    return out

def fit_seasonality_ols(df: pl.DataFrame, target_col: str, feature_cols: list[str]) -> dict:
    # OLS via numpy: beta = (X'X)^(-1) X'y
    X = np.column_stack([np.ones(len(df)), *[df[c].to_numpy() for c in feature_cols]])
    y = df[target_col].to_numpy()
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return {"intercept": beta[0], "betas": dict(zip(feature_cols, beta[1:])),
            "feature_cols": feature_cols}

def apply_seasonality(df: pl.DataFrame, model: dict, as_col: str="s_t") -> pl.DataFrame:
    intercept = model["intercept"]
    feat_cols = model["feature_cols"]
    betas = model["betas"]
    s = intercept
    for c in feat_cols:
        s += df[c].to_numpy() * betas[c]
    return df.with_columns(pl.Series(as_col, s))
