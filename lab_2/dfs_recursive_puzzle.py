from puzzle_logic import get_neighbors


def dfs_recursive(current, goal, visited, parent, steps, depth, max_depth):
    visited.add(current)   # отмечаем текущее состояние как посещённое
    steps[0] += 1          # увеличиваем счётчик шагов

    neighbors = get_neighbors(current)

    # перебираем всех соседей текущего состояния
    for neighbor in neighbors:
        # если дошли до цели — прекращаем поиск
        if current == goal:
            return True

        # если глубина не превышена и сосед ещё не посещён
        if depth < max_depth and neighbor not in visited:
            parent[neighbor] = current  # запоминаем, откуда пришли

            # рекурсивно идём глубже
            if dfs_recursive(neighbor, goal, visited, parent, steps, depth + 1, max_depth):
                return True  # если нашли путь

    return False  # если путь не найден из этой вершины