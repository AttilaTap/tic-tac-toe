import numpy as np
from board import Board
from game_logic import check_game_state

num_states = 3**9
num_actions = 9  # Maximum number of actions per state
Q_table = np.zeros((num_states, num_actions))

# Define the initial and final epsilon values, as well as the number of episodes for the reduction
initial_epsilon = 1
final_epsilon = 0.1
epsilon_reduction_episodes = 400000  # Adjust this based on your preference

# Define gamma and alpha here
gamma = 0.9  # Adjust as needed
alpha = 0.2  # Learning rate

# Calculate the epsilon reduction step
epsilon_step = (initial_epsilon - final_epsilon) / epsilon_reduction_episodes

# Initialize epsilon with the initial value
epsilon = initial_epsilon


def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    else:
        return np.argmax(Q_table[state])


def update_Q_value(state, action, reward, next_state, alpha, gamma):
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


def train_ai(num_episodes, decay_rate, alpha, gamma, check_game_state_fn, save_interval=100000):
    global epsilon  # Ensure epsilon is declared as global

    for episode in range(num_episodes):
        board = Board()  # Initialize a new game
        game_over = False
        current_player = 'X'  # Starting player for the game

        while not game_over:
            state = encode_state(board.board)
            action = choose_action(state, epsilon)
            row, col = action // 3, action % 3

            if board.make_move(row, col, current_player):
                new_state = encode_state(board.board)
                # Pass the game board as an argument
                game_over = check_game_state_fn(board)
                reward = get_reward(board, game_over, current_player)
                update_Q_value(state, action, reward, new_state, alpha, gamma)

                current_player = 'O' if current_player == 'X' else 'X'

        if epsilon > final_epsilon:
            epsilon -= epsilon_step

        if (episode + 1) % save_interval == 0:
            # Save the Q-table periodically
            save_q_table(f"q_table.npy")
            print(f"Save of episode {episode + 1}/{num_episodes} completed")

        if (episode + 1) % 1000 == 0:  # Print every 1000th episode
            print(f"Episode {episode + 1}/{num_episodes} completed")

    # Save the final Q-table after training
    save_q_table()
    print("Training completed and final Q-table saved.")


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


def save_q_table(filename="q_table.npy"):
    np.save(filename, Q_table)


def load_q_table(filename="q_table.npy"):
    global Q_table
    try:
        Q_table = np.load(filename)
    except FileNotFoundError:
        Q_table = np.zeros((num_states, num_actions))


if __name__ == "__main__":
    print("Script started")
    load_q_table()  # Load the trained Q-table
    num_episodes = 2000000  # More episodes might be needed
    decay_rate = 0.999   # Adjust as needed
    alpha = 0.2           # Learning rate
    gamma = 0.9           # Discount factor

    print("Starting training...")

    train_ai(num_episodes, decay_rate, alpha, gamma,
             check_game_state)  # Pass check_game_state function

    print("Training completed.")

    save_q_table()

    print("Q-table saved.")
