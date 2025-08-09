def estimate_uniform_upper_bound(samples):
    """
    Estimate the upper bound 'd' for a uniform distribution [0, d]
    from independent samples.

    Uses the fact that the expected maximum of N samples is (N/(N+1))*d,
    so an unbiased estimator is d_hat = (N+1)/N * max(samples)

    Args:
        samples (list of floats): Observed samples from U(0, d)

    Returns:
        float: Estimated upper bound d
    """

    N = len(samples)
    if N == 0:
        raise ValueError("Input sample array must not be empty")

    observed_max = max(samples)
    unbiased_estimate = (N + 1) / N * observed_max
    return unbiased_estimate


# Example usage
samples = [3.2, 1.5, 2.7, 3.8, 1.9]
estimated_d = estimate_uniform_upper_bound(samples)
print(f"Estimated upper bound d: {estimated_d:.2f}")
