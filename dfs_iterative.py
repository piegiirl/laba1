def restore_path(parent, goal):
    path = [] 

    while goal is not None:
        path.append(goal)     
        goal = parent[goal]   

    return path[::-1] 


def dfs_iterative(graph, start, goal):
    n = len(graph)  # количество вершин

    stack = [start]  # стек, начинаем со стартовой вершины
    visited = set()  # множество посещённых вершин
    parent = {start: None}  # словарь для восстановления пути
    steps = 0  

    # пока стек не пуст
    while stack:
        current = stack.pop()  # берём последний добавленный элемент

        visited.add(current)  # отмечаем вершину как посещённую
        steps += 1

        # перебираем соседей в обратном порядке
        for neighbor in range(n - 1, -1, -1):
            # если нашли цель, то восстанавливаем путь
            if current == goal:
                return restore_path(parent, goal), steps
            # если есть ребро и вершина ещё не посещена
            if graph[current][neighbor] == 1 and neighbor not in visited:
                parent[neighbor] = current  # запоминаем путь
                stack.append(neighbor)      # добавляем в стек

    return None  # если путь не найден