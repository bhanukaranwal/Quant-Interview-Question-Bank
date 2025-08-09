import heapq

class Ant:
    def __init__(self, ant_id, pos, direction, speed):
        self.id = ant_id            # Unique ID
        self.pos = pos              # Current position
        self.speed = speed          # Current speed (positive)
        self.dir = direction        # "left" or "right"
    
    def __repr__(self):
        return f"Ant(id={self.id}, pos={self.pos:.2f}, dir={self.dir}, spd={self.speed})"

def last_ant_variable_speeds(L, ants_data):
    """
    Simulate ants with variable speeds on stick length L to find 
    the last ant and time it falls.
    """

    # Initialize ants sorted by position
    ants = sorted([Ant(**a) for a in ants_data], key=lambda ant: ant.pos)

    # Priority queue for events: (time, type, ant indices)
    # type = "fall" or "collision"
    events = []
    
    def schedule_fall(i):
        """Schedule fall event for ant i"""
        ant = ants[i]
        if ant.dir == "left":
            t_fall = ant.pos / ant.speed
        else:
            t_fall = (L - ant.pos) / ant.speed
        heapq.heappush(events, (t_fall, "fall", (i,)))

    def schedule_collision(i, j):
        """Schedule collision event between ants i and j"""
        a1, a2 = ants[i], ants[j]
        if a1.dir == a2.dir:
            return  # Same direction => no collision
        if a1.dir == "right" and a2.dir == "left":
            rel_speed = a1.speed + a2.speed
            dist = a2.pos - a1.pos
            if rel_speed > 0:
                t_col = dist / rel_speed
                heapq.heappush(events, (t_col, "collision", (i, j)))

    # Initial scheduling
    for i in range(len(ants)):
        schedule_fall(i)
    for i in range(len(ants) - 1):
        schedule_collision(i, i + 1)

    current_time = 0
    alive = [True] * len(ants)
    last_ant_id = None
    last_fall_time = 0

    while events:
        t_event, etype, participants = heapq.heappop(events)
        
        # Advance positions to event time
        dt = t_event - current_time
        for idx, ant in enumerate(ants):
            if alive[idx]:
                if ant.dir == "left":
                    ant.pos -= ant.speed * dt
                else:
                    ant.pos += ant.speed * dt
        current_time = t_event

        if etype == "fall":
            (i,) = participants
            if not alive[i]:
                continue
            alive[i] = False
            last_ant_id = ants[i].id
            last_fall_time = current_time
            # Remove future events involving this ant (lazy skip)
        
        elif etype == "collision":
            i, j = participants
            if not alive[i] or not alive[j]:
                continue
            # Swap directions and speeds (elastic collision for equal mass)
            ants[i].dir, ants[j].dir = ants[j].dir, ants[i].dir
            ants[i].speed, ants[j].speed = ants[j].speed, ants[i].speed
            # Swap IDs because we exchange identities effectively
            ants[i].id, ants[j].id = ants[j].id, ants[i].id
            
            # Reschedule future collisions/falls for these ants
            schedule_fall(i)
            schedule_fall(j)
            if i > 0:
                schedule_collision(i-1, i)
            if j < len(ants)-1:
                schedule_collision(j, j+1)

    return last_ant_id, last_fall_time

# Example Run
L = 10.0
ants_data = [
    {"id": 1, "pos": 2.0, "dir": "right", "speed": 1.5},
    {"id": 2, "pos": 5.0, "dir": "left",  "speed": 1.0},
    {"id": 3, "pos": 8.0, "dir": "left",  "speed": 2.0}
]

last_id, time = last_ant_variable_speeds(L, ants_data)
print(f"Last ant ID: {last_id}, Time: {time:.2f}")
