 
import polars as pl
import numpy as np

def residuals_ar1(df: pl.DataFrame, x_col: str) -> pl.DataFrame:
    x = df[x_col].to_numpy()
    x0, x1 = x[:-1], x[1:]
    phi = np.linalg.lstsq(np.column_stack([np.ones_like(x0), x0]), x1, rcond=None)[0]
    resid = x1 - (phi[0] + phi[1]*x0)
    return pl.DataFrame({"t": df["date"][1:], "resid": resid})

def summary_params(params: dict) -> pl.DataFrame:
    keys, vals = zip(*params.items())
    return pl.DataFrame({"param": keys, "value": vals})
