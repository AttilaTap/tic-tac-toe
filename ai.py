import numpy as np
from board import Board
from game_logic import get_reward, check_game_state

# Constants for AI
num_states = 3**9
num_actions = 9  # Maximum number of actions per state
Q_table = np.zeros((num_states, num_actions))

# AI Parameters
initial_epsilon = 1
final_epsilon = 0.15
epsilon_reduction_episodes = 1500000
gamma = 0.5  # Discount factor
alpha = 0.5  # Learning rate
epsilon = initial_epsilon
epsilon_step = (initial_epsilon - final_epsilon) / epsilon_reduction_episodes


def choose_action(state):
    global epsilon
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    else:
        return np.argmax(Q_table[state])


def update_Q_value(state, action, reward, next_state, alpha, gamma):
    global Q_table
    best_next_action = np.argmax(Q_table[next_state])
    Q_table[state, action] += alpha * \
        (reward + gamma * Q_table[next_state,
         best_next_action] - Q_table[state, action])


def encode_state(board):
    """
    Encode the Tic-Tac-Toe board state into a single integer.

    Args:
    board (list of list of str): The game board.

    Returns:
    int: An integer representing the board state.
    """
    state = 0
    base = 1
    for row in board:
        for cell in row:
            if cell == 'X':
                value = 1
            elif cell == 'O':
                value = 2
            else:  # Empty cell
                value = 0
            state += value * base
            base *= 3
    return state


def decode_state(state):
    """
    Decode the state integer back into a Tic-Tac-Toe board.

    Args:
    state (int): The integer representing the board state.

    Returns:
    list of list of str: The game board.
    """
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            value = state % 3
            if value == 1:
                board[row][col] = 'X'
            elif value == 2:
                board[row][col] = 'O'
            state //= 3
    return board


def save_q_table(filename="q_table.npy"):
    np.save(filename, Q_table)


def load_q_table(filename="q_table.npy"):
    global Q_table
    try:
        Q_table = np.load(filename)
    except FileNotFoundError:
        Q_table = np.zeros((num_states, num_actions))


def train_ai(num_episodes, decay_rate, alpha, gamma, check_game_state_fn, save_interval=100000):
    global epsilon  # Ensure epsilon is declared as global

    for episode in range(num_episodes):
        board = Board()  # Initialize a new game
        game_over = False
        current_player = 'X'  # Starting player for the game
        move_count = 0  # Track number of moves in this episode
        total_reward = 0  # Total reward accumulated in this episode
        q_value_changes = 0  # Track the sum of changes in Q-values

        while not game_over:
            state = encode_state(board.board)
            action = choose_action(state)
            row, col = action // 3, action % 3

            if board.make_move(row, col, current_player):
                new_state = encode_state(board.board)
                game_over = check_game_state_fn(board, current_player)
                reward = get_reward(board, game_over, current_player)

                # Capture old Q-value for logging
                old_q_value = Q_table[state, action]
                update_Q_value(state, action, reward, new_state, alpha, gamma)
                q_value_change = abs(Q_table[state, action] - old_q_value)
                q_value_changes += q_value_change

                current_player = 'O' if current_player == 'X' else 'X'
                move_count += 1
                total_reward += reward

        avg_reward = total_reward / move_count if move_count > 0 else 0
        avg_q_value_change = q_value_changes / move_count if move_count > 0 else 0

        if episode % 1000 == 0:
            avg_reward = total_reward / move_count if move_count > 0 else 0
            avg_q_value_change = q_value_changes / move_count if move_count > 0 else 0
            print(f"Episode {episode + 1}/{num_episodes} completed. Epsilon: {epsilon:.4f}, "
                  f"Moves: {move_count}, Avg Reward: {avg_reward:.4f}, Avg Q-value Change: {avg_q_value_change:.4f}")

        if epsilon > final_epsilon:
            epsilon -= epsilon_step

        if (episode + 1) % save_interval == 0:
            save_q_table(f"q_table.npy")
            print(f"Saved Q-table at episode {episode + 1}")

    save_q_table("q_table.npy")
    print("Training completed. Final Q-table saved.")


if __name__ == "__main__":
    print("Script started")
    load_q_table()  # Load the trained Q-table
    num_episodes = 2000000  # Number of episodes for training
    decay_rate = 0.3   # Adjust as needed
    alpha = 0.2          # Learning rate
    gamma = 0.9          # Discount factor

    print("Starting AI training...")
    train_ai(num_episodes, decay_rate, alpha, gamma, check_game_state)
    print("AI training completed.")
