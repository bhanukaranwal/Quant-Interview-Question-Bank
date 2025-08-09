import numpy as np
from scipy.optimize import minimize

def calibration_objective(params, model_template, market_prices, strikes, T, r):
    # Unpack and set model params
    model = model_template(*params)
    S_paths, _ = model.simulate_paths(T=T, steps=50, n_paths=1000)
    # Price options
    prices = []
    for k in strikes:
        prices.append(price_asian_option(S_paths, np.ones(model.N) / model.N, k, r, T))
    error = np.array(prices) - np.array(market_prices)
    return np.sum(error ** 2)

# Usage example:
# best_params = minimize(calibration_objective, start_guess, args=(model_template, market_data_prices, strikes, T, r))
