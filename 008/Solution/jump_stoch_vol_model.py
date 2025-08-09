import numpy as np

class MultiAssetJumpStochVolModel:
    """Multi-asset jump-stochastic volatility model."""
    def __init__(self, S0, v0, kappa, theta, sigma, rho, lam_jump, mu_jump, sig_jump, corr_matrix):
        self.S0 = np.array(S0)            # Initial prices, size N
        self.v0 = np.array(v0)            # Initial variances, size N
        self.kappa = np.array(kappa)
        self.theta = np.array(theta)
        self.sigma = np.array(sigma)
        self.rho = np.array(rho)
        self.lam_jump = np.array(lam_jump)
        self.mu_jump = np.array(mu_jump)
        self.sig_jump = np.array(sig_jump)
        self.corr_matrix = np.array(corr_matrix)
        self.N = len(S0)

    def simulate_paths(self, T, steps, n_paths, seed=42):
        np.random.seed(seed)
        dt = T / steps
        S_paths = np.zeros((n_paths, steps + 1, self.N))
        v_paths = np.zeros((n_paths, steps + 1, self.N))
        S_paths[:, 0] = self.S0
        v_paths[:, 0] = self.v0
        chol = np.linalg.cholesky(self.corr_matrix)
        for t in range(steps):
            dW = np.dot(np.random.randn(n_paths, self.N), chol) * np.sqrt(dt)
            dZ = np.random.randn(n_paths, self.N) * np.sqrt(dt)
            for i in range(self.N):
                vt = v_paths[:, t, i]
                vt_new = vt + self.kappa[i] * (self.theta[i] - vt) * dt + self.sigma[i] * np.sqrt(np.maximum(vt, 0)) * dZ[:, i]
                v_paths[:, t + 1, i] = np.maximum(vt_new, 1e-8)
                J = np.random.poisson(self.lam_jump[i] * dt, n_paths)
                jump_sum = J * (self.mu_jump[i] + self.sig_jump[i] * np.random.randn(n_paths))
                S_paths[:, t + 1, i] = S_paths[:, t, i] * np.exp(
                    (-vt / 2) * dt + np.sqrt(vt) * dW[:, i] + jump_sum
                )
        return S_paths, v_paths
