from collections import deque  # очередь для BFS


def restore_path(parent, goal):
    path = []  # список для хранения пути

    # идём от цели назад к старту через словарь parent
    while goal is not None:
        path.append(goal)       # добавляем текущую вершину в путь
        goal = parent[goal]     # переходим к родителю

    return path[::-1]  # разворачиваем путь 


def bfs(graph, start, goal):
    n = len(graph)  # количество вершин в графе

    queue = deque([start])  # очередь, начинаем со стартовой вершины
    visited = set()         # множество посещённых вершин
    parent = {start: None}  # словарь для восстановления пути
    steps = 0               

    # пока очередь не пустая
    while queue:
        print(queue)
        print(steps)
        current = queue.popleft()  # берём первый элемент из очереди
        visited.add(current)  # отмечаем как посещённую
        steps += 1  

        # смотрим всех соседей текущей вершины
        for neighbor in range(n):
            # если нашли цель, то восстанавливаем путь
            if current == goal:
                return restore_path(parent, goal), steps
            # если есть ребро между current и neighbor
            if graph[current][neighbor] == 1:
                # если сосед ещё не посещён и не в очереди
                if neighbor not in visited and neighbor not in queue:
                    parent[neighbor] = current  # запоминаем, откуда пришли
                    queue.append(neighbor)      # добавляем в очередь

    return None  # если путь не найден