# Tic-Tac-Toe Game with AI

This is a simple implementation of the classic game of Tic-Tac-Toe (also known as Noughts and Crosses) with an AI opponent. The game is built in Python using the Pygame library for the graphical user interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [AI Training](#ai-training)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- Play Tic-Tac-Toe against an AI opponent.
- The AI opponent uses Q-learning to make decisions.
- Interactive graphical user interface using Pygame.
- Option to start a new game or close the application.
- AI can be trained for different levels of difficulty.

## Installation

To run the game, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/tic-tac-toe-ai.git
    ```

2. **Navigate to the Project Directory**:
   ```bash
   cd tic-tac-toe-ai
    ```

3. **Install Required Dependencies** (using pip):
   ```bash
   pip install pygame numpy
    ```

4. **Run the Game**:
   ```bash
   python main.py
    ```

## How to Play

- Start the game by running main.py.
- The game begins with "X" as the starting player.
- Click on an empty cell to make your move.
- The AI opponent (represented by "O") will make its move automatically.
- Continue taking turns until one player wins or the game ends in a tie.
- The game declares the winner or announces a tie, and you can start a new game.

## AI Training

The AI in this game is trained using Q-learning, a reinforcement learning technique. The training process involves playing multiple episodes of the game to learn optimal strategies. You can customize the training parameters in the #ai.py# file:

- ```num_episodes```: Number of episodes for training.
- ```alpha```: Learning rate.
- ```gamma```: Discount factor.

To train the AI, run the following command:
```bash
python ai.py
```

Training may take some time, depending on the number of episodes and parameters you've set. The trained Q-table will be saved as ```q_table.npy```.

## Project Structure

- ```main.py```: The main game script that handles the GUI and player interactions.
- ```ai.py```: Contains the AI logic, including Q-learning, choosing actions, and updating Q-values.
- ```board.py```: Defines the Board class that represents the game board and checks for wins and ties.
- ```game_logic.py```: Contains functions for calculating rewards and checking the game state.
- ```q_table.npy```: The saved Q-table after training the AI.
- ```README.md```: This readme file.

