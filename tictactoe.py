"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None
OPTIMAL_MAX_X_SCORE = 1
OPTIMAL_MIN_O_SCORE = -1


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

    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).

    """
    x_moves = sum(row.count(X) for row in board)
    o_moves = sum(row.count(O) for row in board)

    if x_moves == o_moves:
        return X  # it's X's move
    return O  # it's O's move
    

def actions(board) -> set[tuple[int, int]]:
    """
    Returns set of all possible actions (i, j) available on the board.

    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    Possible moves are any cells on the board that do not already have an X or an O in them.
    Any return value is acceptable if a terminal board is provided as input.
    """
    possible_actions: set[tuple[int, int]] = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                possible_actions.add((row, column))

    return possible_actions


def result(board, action) -> list[list]:
    """
    Returns the board that results from making move (i, j) on the board.

    If action is not a valid action for the board, your program should raise an exception.
    The returned board state should be the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
    Importantly, the original board should be left unmodified: since Minimax will ultimately require considering many different board states during its computation. This means that simply updating a cell in board itself is not a correct implementation of the result function. You’ll likely want to make a deep copy of the board first before making any changes.
    """
    row = action[0]
    column = action[1]

    # sets the action's cell to the player's symbol
    if board[row][column] != EMPTY:
        raise Exception("Invalid action")
    next_board = copy.deepcopy(board)
    next_board[row][column] = player(board)

    return next_board

def winner(board):
    """
    Returns the winner of the game, if there is one.

    If the X player has won the game, your function should return X. If the O player has won the game, your function should return O.
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
    If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return None.
    """
    winner = None
    
    winner = check_row_wins(board)
    if winner is not None: return winner
    
    winner = check_column_wins(board)
    if winner is not None: return winner
    
    winner = check_diagonal_wins(board)
    if winner is not None: return winner
    
    return None


def check_row_wins(board):
    for row in range(3):
        candidate = board[row][0]
        if candidate is not None and candidate == board[row][1] and candidate == board[row][2]:
            return candidate


def check_column_wins(board):
    for col in range(3):
        candidate = board[0][col]
        if candidate is not None and candidate == board[1][col] and candidate == board[2][col]:
            return candidate

def check_diagonal_wins(board):
    candidate = board[1][1]  # middle cell
    if candidate is not None and (candidate == board[0][0] and candidate == board[2][2]) or \
    (candidate == board[0][2] and candidate == board[2][0]):
        return candidate

def terminal(board) -> bool:
    """
    Returns True if game is over, False otherwise.


    If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return True.
    Otherwise, the function should return False if the game is still in progress.
    """
    # check if someone won the game (there is a three in a row)
    if winner(board) is not None:
        return True
    
    # check if board is full
    return full_board(board)


def full_board(board):
    if all(cell != EMPTY for row in board for cell in row):
        return True
    return False


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

    If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
    You may assume utility will only be called on a board if terminal(board) is True.
    """
    potential_winner = winner(board)
    if potential_winner is X:
        return 1
    elif potential_winner is O:
        return -1
    return 0


def minimax(board) -> tuple[int, int]:
    """
    Returns the optimal action for the current player on the board.

    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves are acceptable.
    If the board is a terminal board, the minimax function should return None.
    """
    if terminal(board):
        return None

    if player(board) == X:
        _, best_action = max_value(board)
        return best_action
    elif player(board) == O:
        _, best_action = min_value(board)
        return best_action
    

def max_value(board) -> tuple[int, tuple[int, int]]:
    if terminal(board):
        return utility(board), None
    
    best_score = -math.inf
    best_action = None

    for action in actions(board):
        next_board = result(board, action)
        score_after_O, _ = min_value(next_board)
        if score_after_O > best_score:
            best_score = score_after_O
            best_action = action
    
    return best_score, best_action


def min_value(board) -> tuple[int, tuple[int, int]]:
    if terminal(board):
        return utility(board), None
    
    best_score = math.inf
    best_action = None

    for action in actions(board):
        next_board = result(board, action)
        score_after_X, _ = max_value(next_board)
        if score_after_X < best_score:
            best_score = score_after_X
            best_action = action

    return best_score, best_action