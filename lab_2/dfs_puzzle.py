from puzzle_logic import get_neighbors


def restore_path(parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]


def dfs(start, goal, max_depth):
    stack = [(start, 0)]
    visited = set()
    parent = {start: None}
    steps = 0

    while stack:
        current, depth = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        steps += 1

        if current == goal:
            return restore_path(parent, goal), steps

        if depth >= max_depth:
            continue

        neighbors = get_neighbors(current)

        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                stack.append((neighbor, depth + 1))

    return None, steps