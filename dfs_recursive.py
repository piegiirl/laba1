def dfs_recursive(graph, current, goal, visited, parent, steps):
    visited.add(current)   # отмечаем текущую вершину как посещённую
    steps[0] += 1          # увеличиваем счётчик шагов

    # перебираем всех соседей текущей вершины
    for neighbor in range(len(graph)):
        # если дошли до цели — прекращаем поиск
        if current == goal:
            return True
        # если есть ребро и сосед ещё не посещён
        if graph[current][neighbor] == 1 and neighbor not in visited:
            parent[neighbor] = current  # запоминаем, откуда пришли

            # рекурсивно идём глубже
            if dfs_recursive(graph, neighbor, goal, visited, parent, steps):
                return True  # если нашли путь

    return False  # если путь не найден из этой вершины