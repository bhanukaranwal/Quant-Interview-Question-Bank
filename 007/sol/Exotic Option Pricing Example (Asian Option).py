def price_asian_option(S_paths, strike, r, T, option_type='call'):
    # Average price over path
    avg_price = np.mean(S_paths[:, 1:], axis=1)
    if option_type == 'call':
        payoff = np.maximum(avg_price - strike, 0)
    else:
        payoff = np.maximum(strike - avg_price, 0)
    # Discounted expected payoff
    return np.exp(-r*T) * np.mean(payoff)
