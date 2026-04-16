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