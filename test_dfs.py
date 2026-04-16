import pytest
from dfs_recursive import dfs_recursive


def run_dfs(graph, start, goal):
    return dfs_recursive(graph, start, goal, set(), [], [0])


# -------------------- БАЗОВЫЕ ТЕСТЫ --------------------

def test_simple_path():
    graph = [
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0],
    ]
    path, steps = run_dfs(graph, 0, 2)

    assert path == [0, 1, 2]
    assert steps >= len(path)


def test_no_path():
    graph = [
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    result = run_dfs(graph, 0, 2)

    assert result is None


def test_start_is_goal():
    graph = [
        [0, 1],
        [0, 0],
    ]
    path, steps = run_dfs(graph, 0, 0)

    assert path == [0]
    assert steps == 1


# -------------------- С ЦИКЛАМИ --------------------

def test_cycle_graph():
    graph = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ]
    path, steps = run_dfs(graph, 0, 2)

    assert path == [0, 1, 2]
    assert steps >= 3


def test_visited_prevents_infinite_loop():
    graph = [
        [0, 1],
        [1, 0],
    ]
    path, steps = run_dfs(graph, 0, 1)

    assert path == [0, 1]
    assert steps >= 2


# -------------------- НЕСКОЛЬКО ПУТЕЙ --------------------

def test_multiple_paths():
    graph = [
        [0, 1, 1],
        [0, 0, 1],
        [0, 0, 0],
    ]
    path, steps = run_dfs(graph, 0, 2)

    assert path in ([0, 1, 2], [0, 2])
    assert steps >= len(path)


# -------------------- BACKTRACKING --------------------

def test_path_backtracking():
    graph = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],  # dead end
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    path, steps = run_dfs(graph, 0, 3)

    assert path == [0, 2, 3]
    assert steps > len(path)  # был заход в тупик → шагов больше


# -------------------- DISCONNECTED --------------------

def test_disconnected_graph():
    graph = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 0, 0],
    ]
    result = run_dfs(graph, 0, 2)

    assert result is None


# -------------------- МАЛЕНЬКИЕ ГРАФЫ --------------------

def test_single_node_success():
    graph = [
        [0],
    ]
    path, steps = run_dfs(graph, 0, 0)

    assert path == [0]
    assert steps == 1


def test_single_node_fail():
    graph = [
        [0],
    ]
    result = run_dfs(graph, 0, 1)

    assert result is None