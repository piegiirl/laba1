from collections import deque
from puzzle_logic import get_neighbors


def restore_path(parent, goal):
    path = []  # список для хранения пути

    # идём от цели к начальному состоянию
    while goal is not None:
        path.append(goal)
        goal = parent[goal]

    return path[::-1]  # разворачиваем путь


def bfs(start, goal):
    queue = deque([start])  # очередь состояний (OPEN)
    visited = set()         # множество посещённых состояний (CLOSED)
    parent = {start: None}  # словарь для восстановления пути
    steps = 0               # счётчик шагов

    # пока есть состояния для обработки
    while queue:
        current = queue.popleft()  # берём первое состояние
        visited.add(current)       # отмечаем как посещённое
        steps += 1
 
        for neighbor in get_neighbors(current):
             # если достигли цели — восстанавливаем путь
            if current == goal:
                return restore_path(parent, goal), steps
            # если состояние ещё не посещено и не в очереди
            if neighbor not in visited and neighbor not in queue:
                parent[neighbor] = current # запоминаем путь
                queue.append(neighbor) # добавляем в очередь
    return None, steps # если решение не найдено