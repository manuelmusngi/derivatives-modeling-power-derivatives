
import numpy as np

class TwoFactorOU:
    def __init__(self, kappa_x, mu_x, sigma_x, kappa_y, mu_y, sigma_y, rho):
        self.kx, self.mx, self.sx = kappa_x, mu_x, sigma_x
        self.ky, self.my, self.sy = kappa_y, mu_y, sigma_y
        self.rho = rho

    def step_xy(self, x_t, y_t, dt, rng=None):
        # exact discretization of OU marginals with correlation via Cholesky
        ex = np.exp(-self.kx * dt)
        ey = np.exp(-self.ky * dt)
        mx = self.mx + (x_t - self.mx) * ex
        my = self.my + (y_t - self.my) * ey
        vx = (self.sx**2) * (1 - ex**2) / (2*self.kx)
        vy = (self.sy**2) * (1 - ey**2) / (2*self.ky)
        # correlated shocks
        z1 = (rng.normal() if rng else np.random.normal())
        z2 = (rng.normal() if rng else np.random.normal())
        eps_x = z1
        eps_y = self.rho * z1 + np.sqrt(1 - self.rho**2) * z2
        return mx + np.sqrt(vx)*eps_x, my + np.sqrt(vy)*eps_y

    def simulate(self, x0, y0, s_t, dt, rng=None):
        x = np.empty_like(s_t, dtype=float)
        y = np.empty_like(s_t, dtype=float)
        x[0], y[0] = x0, y0
        for i in range(1, len(s_t)):
            x[i], y[i] = self.step_xy(x[i-1], y[i-1], dt, rng=rng)
        # log spot: ln S_t = s(t) + x + y
        return np.exp(s_t + x + y)
