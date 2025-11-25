
import numpy as np

def map_to_risk_neutral(mu_p: float, kappa: float, lambda_mpr: float) -> float:
    # mu_Q = mu_P - lambda/kappa
    return mu_p - lambda_mpr / kappa

def estimate_lambda_from_forwards(mu_p, kappa, sigma, s_t_T, x_t, forward_obs, T_minus_t, day_count=365.0):
    # Simple regression-based lambda: fit forward model to observed forwards
    # F_t(T) = E^Q[S_T | F_t] using OU moments -> adjust mu_Q via lambda
    # Here we return a scalar lambda minimizing squared error
    dt = T_minus_t / day_count
    def forward_ou(mu_q):
        m = mu_q + (x_t - mu_q) * np.exp(-kappa * dt)
        v = (sigma**2) * (1 - np.exp(-2*kappa*dt)) / (2*kappa)
        return np.exp(s_t_T + m + 0.5*v)  # lognormal under OU-log spot
    # grid search
    grid = np.linspace(-3.0, 3.0, 121)
    best = None
    for lam in grid:
        mu_q = map_to_risk_neutral(mu_p, kappa, lam)
        err = (forward_ou(mu_q) - forward_obs)**2
        if (best is None) or (err < best[0]):
            best = (err, lam)
    return best[1]
