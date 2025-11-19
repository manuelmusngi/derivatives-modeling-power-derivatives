
import numpy as np

class OneFactorOU:
    def __init__(self, kappa: float, mu: float, sigma: float, use_log: bool=True):
        self.kappa = kappa
        self.mu = mu
        self.sigma = sigma
        self.use_log = use_log

    def step_x(self, x_t: float, dt: float, rng: np.random.Generator|None=None) -> float:
        m = self.mu + (x_t - self.mu) * np.exp(-self.kappa * dt)
        v = (self.sigma**2) * (1 - np.exp(-2*self.kappa*dt)) / (2*self.kappa)
        z = (rng.normal() if rng else np.random.normal())
        return m + np.sqrt(v) * z

    def simulate(self, x0: float, s_t: np.ndarray, dt: float, rng=None) -> np.ndarray:
        x = np.empty_like(s_t, dtype=float)
        x[0] = x0
        for i in range(1, len(s_t)):
            x[i] = self.step_x(x[i-1], dt, rng=rng)
        # Return S_t = exp(s(t) + x_t) or exp(x_t) + s(t) if not log
        if self.use_log:
            return np.exp(s_t + x)
        else:
            return s_t + x
