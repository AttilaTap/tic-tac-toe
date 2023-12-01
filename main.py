import pygame
from board import Board
from ai import choose_action, update_Q_value, encode_state, load_q_table
from game_logic import get_reward, check_game_state

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
BUTTON_COLOR = (150, 150, 150)
BUTTON_HOVER_COLOR = (180, 180, 180)
BUTTON_BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)  # Color for text
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
game_ended = False
game_end_time = 0
alpha = 0.5
gamma = 0.5


def reset_game():
    global game_board, current_player, game_over, winner, buttons_enabled, game_ended
    game_board = Board()
    current_player = "X"
    game_over = False
    winner = None
    buttons_enabled = False
    game_ended = False


def handle_mouse_click(pos):
    global current_player, game_over, winner
    if not game_over:
        row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
        if game_board.make_move(row, col, current_player):
            if game_board.check_tie():  # Check for a tie
                game_over = True
                winner = None  # No winner in a tie
            elif game_board.check_win(current_player):  # Check for a win
                game_over = True
                winner = current_player
            else:
                current_player = "O" if current_player == "X" else "X"


def handle_ai_move():
    global current_player, game_over, winner
    if not game_over and current_player == "O":
        current_state = encode_state(game_board.board)
        action = choose_action(current_state)
        row, col = action // 3, action % 3
        if game_board.make_move(row, col, current_player):
            game_over = check_game_state(game_board, current_player)
            if game_over:
                winner = current_player
            else:
                current_player = "X"
            new_state = encode_state(game_board.board)
            reward = get_reward(game_board, game_over, current_player)
            # Pass alpha and gamma as arguments
            update_Q_value(current_state, action, reward,
                           new_state, alpha, gamma)


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


def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    window.blit(text, text_rect)


def draw_buttons():
    # Define button rectangles
    new_game_button_rect = pygame.Rect(
        NEW_GAME_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    close_button_rect = pygame.Rect(
        CLOSE_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Check if the mouse is over the buttons
    mouse_pos = pygame.mouse.get_pos()
    new_game_button_hovered = new_game_button_rect.collidepoint(mouse_pos)
    close_button_hovered = close_button_rect.collidepoint(mouse_pos)

    # Define button colors
    normal_color = BUTTON_COLOR
    hover_color = BUTTON_HOVER_COLOR

    # Use hover color when the mouse is over a button
    new_game_button_color = hover_color if new_game_button_hovered else normal_color
    close_button_color = hover_color if close_button_hovered else normal_color

    # Draw buttons with gradient effect
    pygame.draw.rect(window, new_game_button_color, new_game_button_rect)
    pygame.draw.rect(window, close_button_color, close_button_rect)

    # Draw button borders
    pygame.draw.rect(window, BUTTON_BORDER_COLOR, new_game_button_rect, 2)
    pygame.draw.rect(window, BUTTON_BORDER_COLOR, close_button_rect, 2)

    # Draw text on buttons
    font = pygame.font.Font(None, 24)
    new_game_text = font.render("New Game", True, TEXT_COLOR)
    close_text = font.render("Close", True, TEXT_COLOR)

    new_game_text_rect = new_game_text.get_rect(
        center=new_game_button_rect.center)
    close_text_rect = close_text.get_rect(center=close_button_rect.center)

    window.blit(new_game_text, new_game_text_rect)
    window.blit(close_text, close_text_rect)


def main():
    global buttons_enabled
    reset_game()
    load_q_table()  # Load the trained Q-table

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == "X":
                handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if NEW_GAME_BUTTON_X <= event.pos[0] <= NEW_GAME_BUTTON_X + BUTTON_WIDTH and \
                        BUTTON_Y <= event.pos[1] <= BUTTON_Y + BUTTON_HEIGHT:
                    reset_game()
                elif CLOSE_BUTTON_X <= event.pos[0] <= CLOSE_BUTTON_X + BUTTON_WIDTH and \
                        BUTTON_Y <= event.pos[1] <= BUTTON_Y + BUTTON_HEIGHT:
                    running = False

        handle_ai_move()

        window.fill(WHITE)
        draw_grid()
        draw_pieces()

        if game_over:
            message = f"Player {winner} wins!" if winner else "It's a tie!"
            display_message(message)
            draw_buttons()
            game_ended = True

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
