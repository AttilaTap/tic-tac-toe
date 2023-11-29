import random
from board import Board


def random_move(board: Board, player):
    empty_spots = [(i, j) for i in range(3)
                   for j in range(3) if board.board[i][j] == " "]
    return random.choice(empty_spots) if empty_spots else None
