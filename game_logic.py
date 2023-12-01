def get_reward(board, game_over, player):
    # Check if the game is over and who the winner is
    if game_over:
        if board.check_win(player):
            if len(player) == 3:  # Check if it's a 3-move win
                return 20  # Assign a high reward for winning in 3 moves
            else:
                return 10  # AI wins
        elif board.check_tie():
            return 0.5  # It's a tie
        else:
            return -10  # Opponent wins
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
                        return 5  # Positive reward for blocking the opponent
                    else:
                        board.board[row][col] = ' '  # Revert the move

        return -0.25  # Penalize each move that doesn't lead to a win or block


def check_game_state(board, current_player):
    if board.check_win(current_player):
        return True
    elif board.check_tie():
        return True
    return False
