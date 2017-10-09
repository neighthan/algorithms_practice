from collections import deque

class Puzzle(object):
    """
    Implement a puzzle data structure for the 8-puzzle.

    Your Puzzle class must define initial_state, goal_state, and next_states(s) as
    specified in the problem statement
    """

    def __init__(self, starting_state):
        """
        __init__(self, starting_state): initializes the Puzzle with the given argument
        as the initial state; must initialize initial_state and goal_state
        ARGS:
          starting_state - the starting state of the puzzle
        """
        self.initial_state = starting_state
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 denotes the blank space

    def __len__(self):
        return 9

    def __getitem__(self, index):
        return self.initial_state[index]  # so you can do Puzzle[i] and get back Puzzle.initial_state[i]

    def __str__(self):
        return str(self.initial_state[:3]) + "\n" + str(self.initial_state[3:6]) + "\n" + str(self.initial_state[6:])

    def __repr__(self):
        return self.__str__()

    def swap(self, state, i, j):
        """
        Swaps two elements in the given state tuple.
        :param state: a tuple with the current state of a puzzle
        :type state: tuple
        :param i: index of one element to swap
        :param j: index of other element to swap; j != i
        :return: a tuple which is a copy of state except the elements at i, j are swapped
        :rtype: tuple
        """
        first = min(i, j)
        second = max(i, j)
        swapped = state[:first] + (state[second],) + state[first + 1:second] + (state[first],) + state[second + 1:]
        # if you make states lists instead of tuples, you can do this more easily, but I wanted them immutable
        return swapped

    def next_states(self, state):
        """
        Returns a list of all the states reachable from the given state with one slide
        :type state: tuple
        :param state: the state from which to
        :rtype: list[tuple]
        :return: a list of states that are reachable with one slide
        """
        next_states = []
        blank_index = state.index(0)  # where the blank spot is; slides have to move a piece to here

        # this is the trickiest part. The slides we can do are left, right, up/top, and down/bottom. However, all of these can only be done if the
        # blank is in the center. If the blank is on the left side, we can't slide left; if on the top, we can't slide up; etc.
        # Thus we check where the blank spot is, and each side that it's not on is a valid direction to move

        left_indices = (0, 3, 6)
        right_indices = (2, 5, 8)
        top_indices = (0, 1, 2)
        bottom_indices = (6, 7, 8)
        left_swap = -1  # sliding left means the index goes down one
        right_swap = 1  # up one for a right slide
        top_swap = -3  # down 3 for a top slide
        bottom_swap = 3  # up three for a bottom slide

        valid_swaps = []
        for indices, swap_value in zip([left_indices, right_indices, top_indices, bottom_indices],
                                       [left_swap, right_swap, top_swap, bottom_swap]):
            if blank_index not in indices: valid_swaps.append(swap_value)

        for swap_value in valid_swaps:
            next_states.append(self.swap(state, blank_index, blank_index + swap_value))

        return next_states


class PuzzleNode(Puzzle):
    """
    Helper class for solving Puzzles. Keeps track of parent PuzzleNode and its own puzzle state as a tuple
    """

    def __init__(self, parent, puzzle_state):
        """
        :param parent:
        :type parent: PuzzleNode
        :param puzzle_state:
        :type puzzle_state: tuple
        :return:
        """

        self.parent = parent
        # super(Puzzle, self).__init__(puzzle_state)
        Puzzle.__init__(self, puzzle_state)

    #     def __str__(self):
    #         if self.parent is None:
    #             return "Parent:\n" + "None" + "\nSelf:\n" + Puzzle.__str__(self)
    #         else:
    #             return "Parent:\n" + Puzzle.__str__(self.parent) + "\nSelf:\n" + Puzzle.__str__(self)

    def get_parent(self):
        return self.parent

    def get_state(self):
        return self.initial_state

    def get_children(self):
        """
        Returns a list of all of the children of the given PuzzleNode
        :return: a list of the children of the given PuzzleNode
        :rtype: list[PuzzleNode]
        """
        return [PuzzleNode(self, state) for state in self.next_states(self.initial_state)]

    def get_path(self):
        """
        :return:
        :rtype: list[tuple]
        """
        if self.parent is None:
            return [self]
        else:
            return self.parent.get_path() + [self]


def solve_puzzle(P):
    """
    Given an 8-puzzle data structure, returns the shortest sequence of states that can be used to solve the puzzle

    :param P: the 8-puzzle, with initial_state, goal_state, and next_states(s) defined
    :type P: Puzzle
    :return: the sequence of states used to solve the puzzle in the fewest moves (as a list); if there are no possible solutions,
             return the empty list
    :rtype: list[tuple]
    """

    # you should be able to just use your BFS implementation from before as long as you standardize your Puzzle class functions
    # (like get_children and is_goal) with those of your Node class; I wrote this code before writing the Node class or the BFS/DFS
    # functions above; it does the same as my BFS, though, except that for unsolvable Puzzles, it doesn't bother trying
    # (it's not meant to be obvious that the parity of the number of inversions shows whether the Puzzle is solvable; there's a proof
    # of that, however)

    puzzle_root = PuzzleNode(None, P.initial_state)
    num_inversions = 0
    for i in range(len(puzzle_root)):
        if puzzle_root[i] == 0: continue  # ignore blank space
        for j in range(i):  # all spaces before this one
            if puzzle_root[j] > puzzle_root[i]:
                num_inversions += 1
    if num_inversions % 2 != 0: return []

    # BFS
    nodes_to_process = deque([puzzle_root])
    nodes_visited = set()
    while nodes_to_process:
        node = nodes_to_process.popleft()
        if node.initial_state in nodes_visited:
            continue
        elif node.initial_state == puzzle_root.goal_state:
            return node.get_path()
        else:
            nodes_visited.add(node.initial_state)
            nodes_to_process.extend(
                [child for child in node.get_children() if child.initial_state not in nodes_visited])
    return []  # if this is reached, there was no valid path


def simple_test():
    # Test the Puzzle class and getting next states
    s = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    P = Puzzle(s)
    assert P.initial_state == (1, 2, 3, 4, 0, 6, 7, 5, 8)
    assert P.goal_state == (1, 2, 3, 4, 5, 6, 7, 8, 0)
    s_next_states = P.next_states(s)
    state_solutions = [(1, 0, 3, 4, 2, 6, 7, 5, 8), (1, 2, 3, 0, 4, 6, 7, 5, 8), (1, 2, 3, 4, 6, 0, 7, 5, 8),
                       (1, 2, 3, 4, 5, 6, 7, 0, 8)]
    for i in range(4):
        assert s_next_states[i] in state_solutions

    # Test finding a solution when the Puzzle is and is not solvable
    unsolvable_puzzles = [Puzzle((5, 1, 8, 0, 2, 3, 4, 6, 7))]
    unsolvable_puzzle_solutions = []
    for puzzle in unsolvable_puzzles:
        unsolvable_puzzle_solutions.append(solve_puzzle(puzzle))
    for solution in unsolvable_puzzle_solutions:
        assert solution == []

    solution_path = [(1, 2, 3, 4, 0, 6, 7, 5, 8), (1, 2, 3, 4, 5, 6, 7, 0, 8), (1, 2, 3, 4, 5, 6, 7, 8, 0)]
    solution = solve_puzzle(P)
    for i in range(len(solution)):
        assert solution[i].initial_state == solution_path[i]
    print("Tests passed.")