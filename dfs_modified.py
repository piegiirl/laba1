def dfs_modified(graph, current, goal, visited, path, steps):
    visited.add(current)   # отмечаем текущую вершину как посещённую
    path.append(current)   # добавляем её в текущий путь
    steps[0] += 1          # увеличиваем счётчик шагов 

    # перебираем всех соседей текущей вершины
    for neighbor in range(len(graph)):
    # если дошли до цели — возвращаем копию пути и количество шагов
        if current == goal:
            return path.copy(), steps[0]
        # если есть ребро и сосед ещё не посещён
        if graph[current][neighbor] == 1 and neighbor not in visited:
            # рекурсивно идём глубже
            result = dfs_modified(graph, neighbor, goal, visited, path, steps)

            # если путь найден — сразу возвращаем результат
            if result:
                return result

    path.pop()  # убираем вершину из пути, если путь не подошёл
    return None  # если путь не найден