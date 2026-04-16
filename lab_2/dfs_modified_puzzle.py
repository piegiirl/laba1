from puzzle_logic import get_neighbors


def dfs_modified(current, goal, visited, path, steps, depth, max_depth):
    visited.add(current)   # отмечаем текущее состояние как посещённое
    path.append(current)   # добавляем его в текущий путь
    steps[0] += 1          # увеличиваем счётчик шагов

    neighbors = get_neighbors(current)

    # перебираем всех соседей текущего состояния
    for neighbor in neighbors:
        # если дошли до цели — возвращаем копию пути и количество шагов
        if current == goal:
            return path.copy(), steps[0]

        # ограничение глубины
        if depth < max_depth and neighbor not in visited:
            # рекурсивно идём глубже
            result = dfs_modified(neighbor, goal, visited, path, steps, depth + 1, max_depth)

            # если путь найден — сразу возвращаем результат
            if result:
                return result

    path.pop()  # убираем состояние из пути, если путь не подошёл
    return None  # если путь не найден