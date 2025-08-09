import numpy as np

def compute_pnl(S_paths, weights):
    final_prices = S_paths[:, -1, :]
    return np.dot(final_prices, weights)

def value_at_risk(pnl, alpha=0.01):
    return np.percentile(pnl, 100 * alpha)

def conditional_var(pnl, alpha=0.01):
    VaR = value_at_risk(pnl, alpha)
    return pnl[pnl <= VaR].mean()

def price_asian_option(S_paths, weights, strike, r, T, option_type='call'):
    avg_price = np.mean(np.dot(S_paths[:, 1:, :], weights), axis=1)
    if option_type == 'call':
        payoff = np.maximum(avg_price - strike, 0)
    else:
        payoff = np.maximum(strike - avg_price, 0)
    return np.exp(-r * T) * np.mean(payoff)
