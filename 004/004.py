def last_ant_falling(ants):
    """
    Determine the last ant to fall off a stick of length 1.

    ants: list of dicts with keys {"id", "pos", "dir"}
        id  -> unique int or str identifier for ant
        pos -> float in (0,1), initial position on stick
        dir -> "left" or "right"
    Returns:
        (last_ant_id, time_last_ant_falls)
    """

    # 1️⃣ Step 1: Compute fall-off times ignoring collisions
    times = []
    for ant in ants:
        if ant["dir"] == "left":
            time = ant["pos"]  # Distance to left end
        else:
            time = 1 - ant["pos"]  # Distance to right end
        times.append(time)

    # Max time = time when last ant falls in "pass-through" world
    max_time = max(times)

    # 2️⃣ Step 2: Now figure out whose ID that corresponds to
    # Here’s the trick:
    # Sort ants by position initially (left to right)
    ants_sorted = sorted(ants, key=lambda a: a["pos"])
    
    # In pass-through world, ants don’t change positions order,
    # but collisions just swap IDs.
    # If one ant falls off right, its ID moves to another ant’s body.

    # Gather indices of ants falling last in pass-through world
    last_indices = [i for i, t in enumerate(times) if abs(t - max_time) < 1e-9]

    # For "pass-through" mapping:
    # - Ant moving right → will be the same as the ith ant from right end falling
    # - Ant moving left → same from left end.
    
    # Get the mapping from "body" to actual ID after swaps
    # This is equivalent to:
    # - If going left, ID is from the leftmost available slot
    # - If going right, ID is from the rightmost available slot
    ids_from_left = [ant["id"] for ant in ants_sorted]   # left to right
    ids_from_right = ids_from_left[::-1]                 # right to left

    last_ant_ids = []
    for idx in last_indices:
        ant = ants[idx]
        if ant["dir"] == "left":
            # In fall-off order to left, this is the idx-th ant in sorted order from left
            sorted_index = sorted(ants, key=lambda a: a["pos"]).index(ant)
            last_ant_ids.append(ids_from_left[sorted_index])
        else:
            sorted_index = sorted(ants, key=lambda a: a["pos"]).index(ant)
            last_ant_ids.append(ids_from_right[sorted_index])

    # Return just one if there's a tie: pick smallest ID for determinism
    return min(last_ant_ids), max_time


# Example usage
ants = [
    {"id": 1, "pos": 0.2, "dir": "right"},
    {"id": 2, "pos": 0.5, "dir": "left"},
    {"id": 3, "pos": 0.8, "dir": "left"}
]

last_id, last_time = last_ant_falling(ants)
print(f"Last ant ID: {last_id}, Time: {last_time:.2f}")
