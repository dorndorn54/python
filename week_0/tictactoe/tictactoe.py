"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # x gets the first move
    # subsequent players alternate with the move

    count_X = 0
    count_O = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                count_X += 1
            if board[row][col] == O:
                count_O += 1
    if count_X > count_O:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # creating the set
    all_possible_sets = set()
    # iterate through each part of the baord and return all possible states if
    # it doesnt have X or O
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:  # to check if empty then give val
                all_possible_sets.add((row, col))  # giving value
    return all_possible_sets


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("the action taken is not an accepted move ")
    # original board left unmodified
    # make a copy of the original board using deep copy
    temp_board = copy.deepcopy(board)
    # action is stored in i j format
    row, col = action
    # make the action to modify the board
    temp_board[row][col] = player(board)
    # return the temp_board back
    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # define the winning conditions
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],  # Top row
        [(1, 0), (1, 1), (1, 2)],  # Middle row
        [(2, 0), (2, 1), (2, 2)],  # Bottom row
        [(0, 0), (1, 0), (2, 0)],  # Left column
        [(0, 1), (1, 1), (2, 1)],  # Middle column
        [(0, 2), (1, 2), (2, 2)],  # Right column
        [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left to bottom-right
        [(0, 2), (1, 1), (2, 0)]   # Diagonal from top-right to bottom-left
    ]
    # if X or O win the game retuen them
    for combination in winning_combinations:
        symbols = [board[row][col] for row, col in combination]
        if symbols.count('X') == 3:
            return X
        if symbols.count('O') == 3:
            return O
    # no winner if game in progress or end in tie
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
