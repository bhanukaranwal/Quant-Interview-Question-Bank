import numpy as np

class MultiAssetStochVolJumpModel:
    def __init__(
        self, S0, v0, kappa, theta, sigma, rho, lambda_jump, mu_jump, sigma_jump, corr_matrix
    ):
        """
        S0: Initial asset prices, shape (N,)
        v0: Initial variances, shape (N,)
        kappa, theta, sigma: Heston parameters, shape (N,)
        rho: Correlation for each asset, shape (N,)
        lambda_jump, mu_jump, sigma_jump: Jump parameters, shape (N,)
        corr_matrix: Brownian correlation, shape (N,N)
        """
        self.S0 = np.array(S0)
        self.v0 = np.array(v0)
        self.kappa = np.array(kappa)
        self.theta = np.array(theta)
        self.sigma = np.array(sigma)
        self.rho = np.array(rho)
        self.lambda_jump = np.array(lambda_jump)
        self.mu_jump = np.array(mu_jump)
        self.sigma_jump = np.array(sigma_jump)
        self.corr_matrix = np.array(corr_matrix)
        self.N = len(S0)
