def simulate_paths(model, T, steps, n_paths, seed=42):
    np.random.seed(seed)
    N = model.N
    dt = T / steps
    S_paths = np.zeros((n_paths, steps + 1, N))
    v_paths = np.zeros((n_paths, steps + 1, N))
    S_paths[:, 0] = model.S0
    v_paths[:, 0] = model.v0

    chol = np.linalg.cholesky(model.corr_matrix)
    for t in range(steps):
        # Generate correlated normals
        dW = np.dot(np.random.randn(n_paths, N), chol) * np.sqrt(dt)
        dZ = np.random.randn(n_paths, N) * np.sqrt(dt)
        for i in range(N):
            vt = v_paths[:, t, i]
            vt_new = (
                vt + model.kappa[i]*(model.theta[i] - vt)*dt + model.sigma[i]*np.sqrt(np.maximum(vt, 0))*dZ[:, i]
            )
            v_paths[:, t+1, i] = np.maximum(vt_new, 1e-8)
            # Jumps
            J = np.random.poisson(model.lambda_jump[i]*dt, n_paths)
            jump_sum = J * (model.mu_jump[i] + model.sigma_jump[i]*np.random.randn(n_paths))
            # Asset Price
            S_paths[:, t+1, i] = S_paths[:, t, i] * np.exp(
                (-(vt/2)*dt) + np.sqrt(vt)*dW[:, i] + jump_sum
            )
    return S_paths
