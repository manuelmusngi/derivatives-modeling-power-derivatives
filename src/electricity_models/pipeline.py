
import polars as pl
from pathlib import Path
from .io import read_spot, read_forwards, write_df
from .cleaning import clip_outliers, add_log_spot
from .features import add_sinusoidal_seasonality, fit_seasonality_ols, apply_seasonality
from .calibration import deseasonalize_log_spot, estimate_ou_mle, estimate_two_factor_cov
from .risk_premia import estimate_lambda_from_forwards, map_to_risk_neutral
from .pricing import forward_one_factor
from .viz import plot_spot, plot_deseasonalized, plot_forward_fit

def run(config: dict):
    # Load
    spot = read_spot(config["paths"]["raw_spot"], config["data"]["date_col"], config["data"]["spot_col"])
    forwards = read_forwards(config["paths"]["raw_forwards"], config["data"]["date_col"], config["data"]["forward_cols"])

    # Clean
    spot = clip_outliers(spot, "spot")
    spot = add_log_spot(spot)

    # Seasonality
    spot = add_sinusoidal_seasonality(spot, freq_per_year=config["seasonality"]["frequency_per_year"],
                                      include_weekly=config["seasonality"]["include_weekly"])
    feat_cols = [c for c in spot.columns if c.startswith(("cos_", "sin_", "dow_"))]
    s_model = fit_seasonality_ols(spot, "log_spot", feat_cols)
    spot = apply_seasonality(spot, s_model, as_col="s_t")

    # Calibration (one-factor)
    x = deseasonalize_log_spot(spot, season_col="s_t")
    dt = 1.0/365.0
    ou_params = estimate_ou_mle(x, dt)

    # Risk premium estimation against one forward maturity (illustrative)
    merged = spot.join(forwards, on="date", how="inner")
    # pick a maturity and its s(T) using same seasonal model but shifted horizon
    T_days = 90
    # approximate s_T as s_t (season function evaluated at T); for demo we reuse s_t
    # in production, compute s(T) from calendar
    lambda_hat = estimate_lambda_from_forwards(ou_params["mu"], ou_params["kappa"], ou_params["sigma"],
                                               merged["s_t"], x_t=x, forward_obs=merged["F_3M"], T_minus_t=T_days)

    mu_q = map_to_risk_neutral(ou_params["mu"], ou_params["kappa"], lambda_hat)

    # Price model forward series
    model_F3M = []
    for i in range(len(merged)):
        s_t_T = merged["s_t"][i]  # placeholder; recompute at T in real use
        x_t_i = x[i]
        model_F3M.append(
            forward_one_factor(mu_q, ou_params["kappa"], ou_params["sigma"], s_t_T, x_t_i, T_days)
        )
    merged = merged.with_columns(pl.Series("F_3M_model", model_F3M))

    # Write processed
    write_df(spot, f'{config["paths"]["interim_dir"]}/spot_clean.csv')
    write_df(merged, f'{config["paths"]["processed_dir"]}/forward_fit.csv')

    # Visualize
    plot_spot(spot, save_path=f'{config["viz"]["save_dir"]}/spot.png')
    plot_deseasonalized(spot, save_path=f'{config["viz"]["save_dir"]}/deseasonalized.png')
    plot_forward_fit(merged, "F_3M", "F_3M_model", save_path=f'{config["viz"]["save_dir"]}/forward_fit_3m.png')

    return {"ou_params": ou_params, "lambda": float(lambda_hat)}
