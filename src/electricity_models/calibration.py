
import numpy as np
import polars as pl
from typing import Dict, Tuple

def deseasonalize_log_spot(df: pl.DataFrame, season_col: str="s_t") -> np.ndarray:
    return (df["log_spot"] - df[season_col]).to_numpy()

def estimate_ou_mle(x: np.ndarray, dt: float) -> Dict[str, float]:
    # Exact discrete-time OU transition: x_{t+1} = a + b x_t + eps, eps ~ N(0, v)
    # Fit AR(1): x_{t+1} = c + phi x_t + e; map to OU
    x0, x1 = x[:-1], x[1:]
    X = np.column_stack([np.ones_like(x0), x0])
    phi = np.linalg.lstsq(X, x1, rcond=None)[0]  # [c_hat, phi_hat]
    c_hat, phi_hat = phi
    # residual variance
    resid = x1 - (c_hat + phi_hat * x0)
    s2 = np.var(resid, ddof=1)
    kappa = -np.log(phi_hat) / dt
    mu = c_hat / (1 - phi_hat)
    sigma = np.sqrt(2 * kappa * s2 / (1 - np.exp(-2*kappa*dt)))
    return {"kappa": float(kappa), "mu": float(mu), "sigma": float(sigma)}

def estimate_two_factor_cov(df: pl.DataFrame, season_col: str="s_t", fast_window: int=7, slow_window: int=90, dt: float=1/365) -> Dict[str, float]:
    # Heuristic split: fast vs slow via smoothing
    x_log = (df["log_spot"] - df[season_col]).to_numpy()
    # slow via moving average
    slow = pl.Series("slow", x_log).rolling_mean(window_size=slow_window, min_periods=1).to_numpy()
    fast = x_log - slow
    # Fit OU parameters for fast/slow separately via AR(1) mapping
    est_x = estimate_ou_mle(fast, dt)
    est_y = estimate_ou_mle(slow, dt)
    # Correlation estimate from residuals
    # For simplicity, compute corr of increments
    dx = np.diff(fast)
    dy = np.diff(slow)
    rho = float(np.corrcoef(dx, dy)[0,1])
    return {
        "kappa_x": est_x["kappa"], "mu_x": est_x["mu"], "sigma_x": est_x["sigma"],
        "kappa_y": est_y["kappa"], "mu_y": est_y["mu"], "sigma_y": est_y["sigma"],
        "rho": rho
    }
