from dfs_iterative import dfs_iterative


def test_dfs_iterative_path():
    graph = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    path, steps = dfs_iterative(graph, 0, 3)

    assert path == [0, 2, 3]
    assert steps >= len(path)


def test_dfs_iterative_no_path():
    graph = [
        [0, 1],
        [0, 0],
    ]
    assert dfs_iterative(graph, 1, 0) is None

graph = [
    [0,1,1,0,0,0,0,0,0,1],
    [0,0,0,0,0,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,1,0,0,0],
]


def test_bfs_0_to_4():
    path, steps = dfs_iterative(graph, 0, 4)

    # кратчайший путь
    assert path == [0, 1, 5, 6, 4]
    assert steps >= len(path)