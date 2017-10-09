import numpy as np
from collections import deque
from typing import List, Tuple, Callable

_up = np.array([-1, 0])
_down = np.array([1, 0])
_left = np.array([0, -1])
_right = np.array([0, 1])


def get_grid_neighbors(node_loc: Tuple[int,int], grid: np.ndarray) -> List[Tuple[int, int]]:
    upper_bounds = np.array(grid.shape) - 1
    lower_bounds = np.array([0, 0])

    neighbors = []
    for direction in [_up, _down, _left, _right]:
        neighbor = np.minimum(np.maximum(node_loc + direction, lower_bounds), upper_bounds)
        if not np.all(neighbor == node_loc):
            neighbors.append(tuple(neighbor))
    return neighbors


def bfs_dfs(start, get_neighbors:Callable, is_goal:Callable[..., bool], algorithm:str,
            get_hashable: Callable=lambda x: x):
    """
    :param start: the initial node
    :param get_neighbors: a function which takes a node (e.g. start) as input and returns its neighbors
    :param is_goal: a function which takes a node (e.g. start) as input and returns whether it's a goal state
    :param algorithm: one of {'bfs', 'dfs'}
    :param get_hashable: a function which returns a hashable version of a node (useful if the nodes themselves aren't)
    :returns:
    """

    fringe = deque()
    expanded = set()  # never expand the same node twice; the first path to any node is the best one
    parents = {}  # parent pointer for each node
    current_node = start
    parent = None

    get_next_node = fringe.pop if algorithm == 'dfs' else fringe.popleft


    while True:
        expanded.add(get_hashable(current_node))
        parents[get_hashable(current_node)] = parent

        if is_goal(current_node):
            break

        neighbors = [(neighbor, current_node) for neighbor in get_neighbors(current_node) if get_hashable(neighbor) not in expanded]
        fringe.extend(neighbors)

        while get_hashable(current_node) in expanded:
            current_node, parent = get_next_node()

    # construct path as list of nodes: [start, ..., goal]
    path = [current_node] # last node was a goal state
    parent = parents[get_hashable(current_node)]
    while parent is not None:
        path.append(parent)
        parent = parents[get_hashable(parent)]
    path.reverse()  # because we started at the goal
    return path