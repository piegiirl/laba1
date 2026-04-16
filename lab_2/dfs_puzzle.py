from puzzle_logic import get_neighbors


def restore_path(parent, goal):
    path = []  # список для хранения пути
    # идём от цели к начальному состоянию
    while goal is not None:
        path.append(goal)
        goal = parent[goal]

    return path[::-1]  # разворачиваем путь


def dfs(start, goal, max_depth):
    stack = [(start, 0)]  # стек: (состояние, глубина)
    visited = set()       # множество посещённых состояний
    parent = {start: None}  # словарь для восстановления пути
    steps = 0             # счётчик шагов

    # пока стек не пуст
    while stack:
        current, depth = stack.pop()  # берём последнее состояние

        # если уже посещали — пропускаем
        if current in visited:
            continue

        visited.add(current)  # отмечаем как посещённое
        steps += 1

        # ограничение глубины поиска
        if depth >= max_depth:
            continue

        # генерируем соседние состояния
        neighbors = get_neighbors(current)

        # добавляем в стек (в обратном порядке для корректного обхода)
        for neighbor in reversed(neighbors):
                    # проверка достижения цели
            if current == goal:
                return restore_path(parent, goal), steps
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current  # запоминаем путь
                stack.append((neighbor, depth + 1))  # добавляем в стек

    return None, steps  # если решение не найдено