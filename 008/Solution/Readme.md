# Multi-Asset Optimal Portfolio and Derivative Pricing in Jump-Stochastic Volatility Markets

This solution includes:
- Mathematical background
- Model and simulation code
- Derivative pricing and risk metrics
- Calibration routine outline
- PIDE solver schematic for optimal control

See `jump_stoch_vol_model.py`, `pricing_and_risk.py`, `calibration.py`, `pide_solver.py`.

## How to use

1. Build your model and calibrate parameters (see calibration.py).
2. Simulate asset paths (`simulate_paths`).
3. Price derivatives and compute risk (VaR/CVaR).
4. (Optional) Solve for optimal portfolio/consumption by dynamic programming and PIDE solution.

You may extend with Fourier-based pricing, parallel simulation, or additional Monte Carlo features as needed for research or production.
