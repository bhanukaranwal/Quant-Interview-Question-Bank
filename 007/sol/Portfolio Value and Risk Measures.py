def compute_portfolio_pnl(S_paths, portfolio_weights):
    # Assuming portfolio is linear in terminal prices
    final_prices = S_paths[:, -1, :]
    return np.dot(final_prices, portfolio_weights)

def value_at_risk(pnl, alpha=0.01):
    return np.percentile(pnl, 100*alpha)

def conditional_var(pnl, alpha=0.01):
    var = value_at_risk(pnl, alpha)
    return pnl[pnl <= var].mean()
