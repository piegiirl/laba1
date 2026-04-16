from puzzle_logic import get_neighbors


def dfs_recursive_search(current, goal, depth, max_depth, path, visited, steps):
    steps[0] += 1

    if current == goal:
        return path[:]

    if depth >= max_depth:
        return None

    for neighbor in get_neighbors(current):
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)

            result = dfs_recursive_search(
                neighbor, goal, depth + 1, max_depth, path, visited, steps
            )

            if result is not None:
                return result

            path.pop()
            visited.remove(neighbor)

    return None


def dfs_recursive(start, goal, max_depth):
    steps = [0]
    path = [start]
    visited = {start}

    result = dfs_recursive_search(start, goal, 0, max_depth, path, visited, steps)
    return result, steps[0]