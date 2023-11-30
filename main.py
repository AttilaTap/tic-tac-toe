import pygame
import numpy as np
from board import Board
from game_logic import get_reward
from ai import get_reward, choose_action, update_Q_value, encode_state, load_q_table, epsilon, gamma, alpha

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

# Initialize Pygame and Game Window
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Tic-Tac-Toe")

# Game State Initialization
game_board = Board()
current_player = "X"
game_over = False
winner = None
buttons_enabled = False
game_end_time = 0


def check_game_state():
    global game_over, winner, game_end_time
    if game_board.check_win(current_player):
        game_over = True
        winner = current_player
    elif game_board.check_tie():
        game_over = True
        winner = None
    if game_over:
        game_end_time = pygame.time.get_ticks()
        pygame.time.set_timer(pygame.USEREVENT, BUTTON_ENABLE_DELAY)
    return game_over  # Add this line to return the game_over status


def reset_game():
    global game_board, current_player, game_over, winner, buttons_enabled
    game_board = Board()
    current_player = "X"
    game_over = False
    winner = None
    buttons_enabled = False


def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(window, LINE_COLOR, (0, i * CELL_SIZE),
                         (WINDOW_SIZE, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(window, LINE_COLOR, (i * CELL_SIZE, 0),
                         (i * CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)


def draw_pieces():
    for row in range(3):
        for col in range(3):
            piece = game_board.board[row][col]
            center = (col * CELL_SIZE + CELL_SIZE // 2,
                      row * CELL_SIZE + CELL_SIZE // 2)
            if piece == "X":
                pygame.draw.line(window, BLUE, (center[0] - X_OFFSET, center[1] - X_OFFSET),
                                 (center[0] + X_OFFSET, center[1] + X_OFFSET), LINE_WIDTH)
                pygame.draw.line(window, BLUE, (center[0] + X_OFFSET, center[1] - X_OFFSET),
                                 (center[0] - X_OFFSET, center[1] + X_OFFSET), LINE_WIDTH)
            elif piece == "O":
                pygame.draw.circle(window, RED, center, O_RADIUS, LINE_WIDTH)


def handle_mouse_click(pos):
    global current_player, game_over
    if not game_over:
        row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
        if game_board.make_move(row, col, current_player):
            check_game_state()
            if not game_over:
                current_player = "O"


def handle_ai_move():
    global current_player, game_over
    if not game_over and current_player == "O":
        current_state = encode_state(game_board.board)
        action = choose_action(current_state, epsilon)
        row, col = action // 3, action % 3

        if game_board.board[row][col] == ' ':
            game_board.make_move(row, col, current_player)
            game_over = check_game_state()  # Update this to return game_over status
            reward = get_reward(game_board, game_over,
                                current_player)  # Get the reward

            new_state = encode_state(game_board.board)
            update_Q_value(current_state, action, reward,
                           new_state, alpha, gamma)

            if not game_over:
                current_player = "X"


def draw_button(text, x, y, w, h, action=None):
    global game_end_time
    current_time = pygame.time.get_ticks()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)
    button_color = (170, 170, 170) if button_rect.collidepoint(
        mouse) else (100, 100, 100)
    pygame.draw.rect(window, button_color, button_rect)
    text_surf = pygame.font.Font(None, 20).render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    window.blit(text_surf, text_rect)

    if buttons_enabled and button_rect.collidepoint(mouse) and click[0] == 1 and action:
        if current_time - game_end_time > BUTTON_PRESS_DELAY:
            action()


def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    window.blit(text, text_rect)


def main():
    global buttons_enabled
    reset_game()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Set running to False to exit the game loop
            elif event.type == pygame.USEREVENT:
                buttons_enabled = True
                pygame.time.set_timer(pygame.USEREVENT, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == "X":
                handle_mouse_click(event.pos)

        handle_ai_move()

        window.fill(WHITE)
        draw_grid()
        draw_pieces()

        if game_over:
            message = f"Player {winner} wins!" if winner else "It's a tie!"
            display_message(message)
            draw_button("New Game", NEW_GAME_BUTTON_X, BUTTON_Y,
                        BUTTON_WIDTH, BUTTON_HEIGHT, reset_game)
            draw_button("Close", CLOSE_BUTTON_X, BUTTON_Y,
                        BUTTON_WIDTH, BUTTON_HEIGHT, pygame.quit)

        # Check if Pygame is initialized before updating the display
        pygame.display.update() if pygame.get_init() else None


if __name__ == "__main__":
    print("Script started")
    load_q_table()  # Load the trained Q-table
    main()  # Start the main game loop
    pygame.quit()  # This line should be outside the main function
