# solver.py
import heapq
from collections import deque

GOAL_STATE = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)

def get_neighbors(state):
    neighbors = []
    zero_pos = [(r, c) for r in range(3) for c in range(3) if state[r][c] == 0][0]
    r, c = zero_pos
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

def manhattan_distance(state):
    distance = 0
    goal_positions = {val: (r, c) for r, row in enumerate(GOAL_STATE) for c, val in enumerate(row)}
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:
                gr, gc = goal_positions[val]
                distance += abs(r - gr) + abs(c - gc)
    return distance

def bfs(start):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current == GOAL_STATE:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                queue.append((neighbor, path + [current]))
    return None

def astar(start):
    heap = [(manhattan_distance(start), 0, start, [])]
    visited = set()
    while heap:
        est_total, cost, current, path = heapq.heappop(heap)
        if current == GOAL_STATE:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + 1 + manhattan_distance(neighbor), cost + 1, neighbor, path + [current]))
    return None
