import heapq

class Ant:
    def __init__(self, ant_id, pos, dir, speed, mass):
        self.id = ant_id
        self.pos = pos
        self.vel = speed if dir == "right" else -speed  # velocity signed
        self.mass = mass
        self.alive = True
        self.last_update_time = 0.0
    
    def advance(self, t):
        """Advance the position to time t."""
        dt = t - self.last_update_time
        self.pos += self.vel * dt
        self.last_update_time = t
    
    def __repr__(self):
        return f"Ant({self.id}, pos={self.pos:.3f}, vel={self.vel:.3f}, m={self.mass})"

def schedule_fall_event(ant, stick_length):
    """Compute fall time for one ant."""
    if ant.vel > 0:
        t = (stick_length - ant.pos) / ant.vel
    else:
        t = ant.pos / abs(ant.vel)
    return t

def schedule_collision_event(a1, a2):
    """Compute collision time between two ants moving towards each other."""
    if a1.vel <= a2.vel:  # Not approaching
        return None
    rel_speed = a1.vel - a2.vel
    if rel_speed <= 0:
        return None
    dist = a2.pos - a1.pos
    if dist <= 0:
        return None
    return dist / rel_speed

def last_ant_physics(L, ants_data):
    # Sort ants by position initially
    ants = sorted(
        [Ant(**data) for data in ants_data],
        key=lambda a: a.pos
    )
    N = len(ants)
    
    # Priority queue of events (time, type, ant_indices)
    events = []
    current_time = 0.0
    
    # Schedule initial falls
    for i, ant in enumerate(ants):
        t_fall = schedule_fall_event(ant, L)
        heapq.heappush(events, (current_time + t_fall, "fall", (i,)))
    
    # Schedule initial collisions between neighbors
    for i in range(N - 1):
        t_col = schedule_collision_event(ants[i], ants[i+1])
        if t_col:
            heapq.heappush(events, (current_time + t_col, "collision", (i, i+1)))
    
    last_ant_id = None
    last_fall_time = 0.0

    while events:
        t_event, etype, participants = heapq.heappop(events)
        
        # Advance all ants to t_event
        for ant in ants:
            if ant.alive:
                ant.advance(t_event)
        current_time = t_event
        
        if etype == "fall":
            (i,) = participants
            ant = ants[i]
            if not ant.alive:
                continue
            ant.alive = False
            last_ant_id = ant.id
            last_fall_time = current_time
            
        elif etype == "collision":
            i, j = participants
            a1, a2 = ants[i], ants[j]
            if not (a1.alive and a2.alive):
                continue
            if a1.pos >= a2.pos:
                continue
            # Perform elastic collision velocity update
            m1, m2 = a1.mass, a2.mass
            u1, u2 = a1.vel, a2.vel
            v1 = (u1*(m1 - m2) + 2*m2*u2) / (m1 + m2)
            v2 = (u2*(m2 - m1) + 2*m1*u1) / (m1 + m2)
            a1.vel, a2.vel = v1, v2
            
            # Reschedule falls
            t_fall_i = schedule_fall_event(a1, L)
            t_fall_j = schedule_fall_event(a2, L)
            heapq.heappush(events, (current_time + t_fall_i, "fall", (i,)))
            heapq.heappush(events, (current_time + t_fall_j, "fall", (j,)))
            # Reschedule neighbor collisions
            if i > 0:
                t_col_prev = schedule_collision_event(ants[i-1], a1)
                if t_col_prev:
                    heapq.heappush(events, (current_time + t_col_prev, "collision", (i-1, i)))
            if j < N - 1:
                t_col_next = schedule_collision_event(a2, ants[j+1])
                if t_col_next:
                    heapq.heappush(events, (current_time + t_col_next, "collision", (j, j+1)))
    
    return last_ant_id, last_fall_time

# Example run
L = 10.0
ants_data = [
    {"ant_id": 1, "pos": 2.0, "dir": "right", "speed": 1.5, "mass": 1.0},
    {"ant_id": 2, "pos": 5.0, "dir": "left",  "speed": 1.0, "mass": 2.0},
    {"ant_id": 3, "pos": 8.0, "dir": "left",  "speed": 2.0, "mass": 1.5}
]

last_id, last_time = last_ant_physics(L, ants_data)
print(f"Last ant ID: {last_id}, Time: {last_time:.4f}")
