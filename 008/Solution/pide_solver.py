def solve_pide(V, grid, jumps, dt, utility_fn, constraints):
    """
    V: value function grid
    grid: multidimensional mesh (asset prices, volatility, wealth, time)
    jumps: jump parameters
    dt: time increment
    utility_fn: CRRA or other utility
    constraints: feasible set of portfolio choices
    
    Returns: Updated value function grid
    """
    # For each time step backwards:
    #   - Apply finite difference for diffusion
    #   - Compute jump integral with quadrature/interpolation
    #   - At each node, maximize over portfolio/consumption
    #   - Update V
    pass  # Full implementation: large; see solution outline above
