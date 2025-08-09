from jump_stoch_vol_model import MultiAssetJumpStochVolModel
from pricing_and_risk import price_asian_option, compute_pnl, value_at_risk, conditional_var

# Parameter setup for example
N = 3
S0 = [100, 90, 80]
v0 = [0.04, 0.05, 0.03]
kappa = [2, 3, 2]
theta = [0.04, 0.05, 0.04]
sigma = [0.2, 0.25, 0.2]
rho = [0.2, 0.3, 0.1]
lam_jump = [0.05, 0.07, 0.08]
mu_jump = [-0.02, -0.01, -0.03]
sig_jump = [0.03, 0.02, 0.02]
corr_matrix = np.array([[1,0.3,0.2],[0.3,1,0.25],[0.2,0.25,1]])

# Build model
model = MultiAssetJumpStochVolModel(S0, v0, kappa, theta, sigma, rho, lam_jump, mu_jump, sig_jump, corr_matrix)
S_paths, _ = model.simulate_paths(T=1.0, steps=252, n_paths=10000)

# Asian option pricing
price = price_asian_option(S_paths, weights=np.ones(N)/N, strike=95, r=0.01, T=1.0)

# Portfolio risk metrics
weights = [0.5, 0.3, 0.2]
pnl = compute_pnl(S_paths, weights)
VaR = value_at_risk(pnl, alpha=0.01)
CVaR = conditional_var(pnl, alpha=0.01)

print("Asian option price: ", price)
print("Portfolio VaR (99%): ", VaR)
print("Portfolio CVaR (99%): ", CVaR)
