import random

SIZE = 4  


def get_neighbors(state):
    neighbors = []  # список соседних состояний

    zero = state.index(0)  # находим позицию пустой клетки (0)
    x, y = divmod(zero, SIZE)  # переводим индекс в координаты (строка, столбец)

    # возможные движения: вверх, вниз, влево, вправо
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy  # новые координаты после движения

        # проверка: не вышли ли за границы поля
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            new_state = list(state)  # копируем текущее состояние

            new_zero = nx * SIZE + ny  # индекс новой позиции пустой клетки

            # меняем местами 0 и соседнюю плитку
            new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]

            neighbors.append(tuple(new_state))  # добавляем новое состояние

    return neighbors  # возвращаем все возможные ходы

def shuffle_board(steps=5):
    # начинаем с решённого состояния
    board = list(range(1, 16)) + [0]

    prev = None  # предыдущее состояние (чтобы не возвращаться назад)

    for _ in range(steps):
        neighbors = get_neighbors(tuple(board))  # получаем возможные ходы

        # убираем состояние, из которого пришли
        if prev and prev in neighbors:
            neighbors.remove(prev)

        next_state = random.choice(neighbors)  # случайный следующий ход

        prev = tuple(board)   # запоминаем текущее состояние
        board = list(next_state)  # переходим в новое состояние

    return board  # возвращаем перемешанную доску