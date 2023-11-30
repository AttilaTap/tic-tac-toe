import pygame
import numpy as np
from board import Board

# Constants
WINDOW_SIZE = 300
CELL_SIZE = WINDOW_SIZE // 3
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 2
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
X_OFFSET = 40
O_RADIUS = 40
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
NEW_GAME_BUTTON_X = 50
CLOSE_BUTTON_X = WINDOW_SIZE - 150
BUTTON_Y = WINDOW_SIZE - 60
BUTTON_PRESS_DELAY = 500  # in milliseconds
BUTTON_ENABLE_DELAY = 1000  # in milliseconds

# Game State Initialization
game_board = Board()
current_player = "X"
game_over = False
winner = None
buttons_enabled = False
game_end_time = 0

# Initialize Pygame and Game Window
pygame.init()


def check_game_state(board):
    global game_over, winner, game_end_time
    if board.check_win(current_player):
        game_over = True
        winner = current_player
    elif board.check_tie():
        game_over = True
        winner = None
    if game_over:
        game_end_time = pygame.time.get_ticks()
        pygame.time.set_timer(pygame.USEREVENT, BUTTON_ENABLE_DELAY)
    return game_over


def reset_game():
    global game_board, current_player, game_over, winner, buttons_enabled
    game_board = Board()
    current_player = "X"
    game_over = False
    winner = None
    buttons_enabled = False


def get_reward(board, game_over, player):
    # Check if the game is over and who the winner is
    if game_over:
        if board.check_win(player):
            return 2  # AI wins
        elif board.check_tie():
            return 0.5  # It's a tie
        else:
            return -1  # Opponent wins
    else:
        # Check for potential opponent wins in rows, columns, and diagonals
        opponent = "X" if player == "O" else "O"
        for row in range(3):
            for col in range(3):
                if board.board[row][col] == ' ':
                    # Simulate the opponent's move
                    board.board[row][col] = opponent
                    if board.check_win(opponent):
                        # If the opponent wins with this move, block it
                        board.board[row][col] = ' '  # Revert the move
                        return 1  # Positive reward for blocking the opponent
                    else:
                        board.board[row][col] = ' '  # Revert the move

        return -0.1  # Penalize each move that doesn't lead to a win or block
