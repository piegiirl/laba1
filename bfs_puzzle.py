from collections import deque
from puzzle_logic import get_neighbors


def restore_path(parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]


def bfs(start, goal):
    queue = deque([start])
    visited = set()
    parent = {start: None}
    steps = 0

    while queue:
        current = queue.popleft()
        visited.add(current)
        steps += 1
 
        for neighbor in get_neighbors(current):
            if current == goal:
                return restore_path(parent, goal), steps
            if neighbor not in visited and neighbor not in queue:
                parent[neighbor] = current
                queue.append(neighbor)
    return None, steps