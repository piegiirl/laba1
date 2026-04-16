from puzzle_logic import get_neighbors


def restore_path(parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]


def is_in_path(parent, current, node):
    while current is not None:
        if current == node:
            return True
        current = parent[current]
    return False


def dfs_modified(start, goal, max_depth):
    stack = [(start, 0)]
    parent = {start: None}
    steps = 0

    while stack:
        current, depth = stack.pop()
        steps += 1

        if current == goal:
            return restore_path(parent, current), steps

        if depth >= max_depth:
            continue

        neighbors = get_neighbors(current)

        for neighbor in reversed(neighbors):
            if not is_in_path(parent, current, neighbor):
                parent[neighbor] = current
                stack.append((neighbor, depth + 1))

    return None, steps