from dfs_modified import dfs_modified


def run(graph, start, goal):
    return dfs_modified(graph, start, goal, set(), [], [0])


def test_modified_path():
    graph = [
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    path, steps = run(graph, 0, 3)

    assert path == [0, 2, 3]
    assert steps >= len(path)


def test_modified_no_path():
    graph = [
        [0, 1],
        [0, 0],
    ]
    assert run(graph, 1, 0) is None