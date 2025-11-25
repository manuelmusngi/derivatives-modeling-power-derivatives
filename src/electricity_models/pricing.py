
import numpy as np

def forward_one_factor(mu_q, kappa, sigma, s_t_T, x_t, T_minus_t, day_count=365.0):
    dt = T_minus_t / day_count
    m = mu_q + (x_t - mu_q) * np.exp(-kappa * dt)
    v = (sigma**2) * (1 - np.exp(-2*kappa*dt)) / (2*kappa)
    return np.exp(s_t_T + m + 0.5*v)

def forward_two_factor(params_q, s_t_T, x_t, y_t, T_minus_t, day_count=365.0):
    kx, mxq, sx = params_q["kx"], params_q["mxq"], params_q["sx"]
    ky, myq, sy = params_q["ky"], params_q["myq"], params_q["sy"]
    rho = params_q["rho"]
    dt = T_minus_t / day_count
    ex, ey = np.exp(-kx*dt), np.exp(-ky*dt)
    mx = mxq + (x_t - mxq) * ex
    my = myq + (y_t - myq) * ey
    vx = (sx**2) * (1 - ex**2) / (2*kx)
    vy = (sy**2) * (1 - ey**2) / (2*ky)
    # zero cross term in variance for log spot expectation (mean only needs sum), but
    # variance of log S includes correlation; expectation uses 0.5 * total variance
    v_tot = vx + vy + 2*rho*np.sqrt(vx*vy)
    return np.exp(s_t_T + mx + my + 0.5*v_tot)
