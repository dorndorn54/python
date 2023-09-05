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
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # creating the set
    all_possible_sets = set()
    # iterate through each part of the board and return all possible states if
    # it doesnt have X or O
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:  # to check if empty then give val
                all_possible_sets.add((row, col))  # giving value
    return all_possible_sets


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        return Exception("action not valid")
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
    # if X or O win the game return them
    for combination in winning_combinations:
        symbols = [board[row][col] for row, col in combination]
        if symbols.count('X') == 3:
            return X
        if symbols.count('O') == 3:
            return O
    # no winner if game in progress or end in tie
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if someone won or all cells filled retun true
    if winner(board) == X or winner(board) == O:
        return True
    # check if all cells are filled if so return True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                return False
    # if got tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # if it is the maximising players X turn
    elif player(board) == X:
        # provide all the potential next moves on the board
        plays = []
        for action in actions(board):
            plays.append([min_value(result(board, action)), action])
        return sorted(plays, key=lambda X: X[0], reverse=True)[0][1]

    # if it is the minimising players O turn
    elif player(board) == O:
        plays = []
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=lambda O: O[0])[0][1]
    # provide all the potential next moves on the board
    # pass it through the max_value() function so it gives the best option
