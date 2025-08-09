def egg_drop(n, m):
    """
    Calculate minimum number of drops needed in worst case with n eggs and m floors.

    Parameters:
    n (int): Number of eggs
    m (int): Number of floors

    Returns:
    int: Minimum number of drops in worst case
    """

    # dp[i][j] = minimum number of attempts needed for i eggs and j floors
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Base cases:
    # With one egg, we need j drops in worst case (linear search)
    for j in range(m + 1):
        dp[1][j] = j

    # With zero floors, zero drops needed; with one floor, one drop needed
    for i in range(1, n + 1):
        dp[i][0] = 0
        dp[i][1] = 1

    # Fill dp table for i eggs and j floors
    for i in range(2, n + 1):
        for j in range(2, m + 1):
            # Initialize with a large number
            dp[i][j] = float('inf')

            # We want to minimize the maximum drops needed in worst case:
            # If egg breaks, check floors below; if not, check above floors
            # We test dropping from floor x (1 to j), so max of these two cases plus one drop
            # We choose x to minimize this maximum
            # This brute force is O(n*m^2), but works for moderate inputs.

            for x in range(1, j + 1):
                # max of two scenarios:
                # Egg breaks: check floors below with one less egg (x-1 floors)
                # Egg doesn't break: check above floors (j - x floors) with same eggs
                res = 1 + max(dp[i-1][x-1], dp[i][j-x])
                if res < dp[i][j]:
                    dp[i][j] = res

    return dp[n][m]


# Example usage
N = 2
M = 6
result = egg_drop(N, M)
print(f"Minimum drops with {N} eggs and {M} floors: {result}")
