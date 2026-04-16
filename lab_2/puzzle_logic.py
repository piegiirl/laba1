import random

SIZE = 4


def get_neighbors(state):
    neighbors = []
    zero = state.index(0)
    x, y = divmod(zero, SIZE)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            new_state = list(state)
            new_zero = nx * SIZE + ny

            new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]
            neighbors.append(tuple(new_state))

    return neighbors


def is_solvable(board):
    inv = 0
    arr = [x for x in board if x != 0]

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    row_from_bottom = 4 - (board.index(0) // 4)

    return (inv + row_from_bottom) % 2 == 1

def shuffle_board(steps=5):
    board = list(range(1, 16)) + [0]
    prev = None

    for _ in range(steps):
        neighbors = get_neighbors(tuple(board))

        # убираем состояние, из которого пришли (анти-откат)
        if prev and prev in neighbors:
            neighbors.remove(prev)

        next_state = random.choice(neighbors)
        prev = tuple(board)
        board = list(next_state)

    return board