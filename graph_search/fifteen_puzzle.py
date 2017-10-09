import numpy as np
from utils import get_grid_neighbors
from typing import Sequence, Union, Optional, List, Tuple, Callable, Any

_OneOrMore = lambda type_: Union[type_, Sequence[type_]]


def _get_shape_and_size(shape:_OneOrMore(int)) -> Tuple[Tuple[int, int], int]:
    shape = (shape,) * 2 if type(shape) == int else shape
    assert len(shape) == 2
    size = np.prod(shape)
    return shape, size


def get_puzzle(shape: _OneOrMore(int)=15, solvable_only: bool=True) -> np.ndarray:
    """
    0 denotes the blank space.
    :param shape: the shape of the puzzle. If an int is given, it will be a square of that size. If two ints are given,
                  it will be a rectangle of that shape.
    :param solvable_only: try to only return solvable puzzles; this isn't a guarantee
    :returns:
    """

    shape, size = _get_shape_and_size(shape)

    if not solvable_only:
        return np.random.permutation(np.arange(size)).reshape(shape)

    num_inversions = 1 # so that we go into the while loop
    while num_inversions % 2 != 0:
        puzzle = np.random.permutation(np.arange(size)).reshape(shape)
        puzzle_1d = puzzle.ravel()

        num_inversions = 0
        for i in range(len(puzzle_1d)):
            if puzzle_1d[i] == 0: continue  # ignore blank space
            for j in range(i):  # all spaces before this one
                if puzzle_1d[j] > puzzle_1d[i]:
                    num_inversions += 1

    return puzzle


def get_goal_state(shape: _OneOrMore(int)=15) -> np.ndarray:
    """
    0 denotes the blank space.
    :param shape: the shape of the puzzle. If an int is given, it will be a square of that size. If two ints are given,
                  it will be a rectangle of that shape.
    :returns:
    """
    shape, size = _get_shape_and_size(shape)
    return np.concatenate((np.arange(1, size), [0])).reshape(shape)


def next_states(state: np.ndarray) -> List[np.ndarray]:
    """
    :returns: a list of all the states reachable from the current state with one slide
    """

    next_states = []
    x, y = np.where(state == 0)
    zero_idx = (x[0], y[0])
    valid_moves = get_grid_neighbors(zero_idx, state)
    for move in valid_moves:
        new_state = state.copy()
        new_state[zero_idx] = new_state[move]
        new_state[move] = 0
        next_states.append(new_state)

    return next_states
