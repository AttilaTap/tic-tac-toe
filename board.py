class Board:
    def __init__(self):
        # Initialize the board with empty spaces
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col, player):
        if self.board[row][col] == " ":
            self.board[row][col] = player
            return True
        return False

    def check_win(self, player):
        # Check all rows, columns and diagonals for a win
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]) or \
               all([self.board[j][i] == player for j in range(3)]):
                return True

        if all([self.board[i][i] == player for i in range(3)]) or \
           all([self.board[i][2 - i] == player for i in range(3)]):
            return True

        return False

    def check_tie(self):
        # Check if all spaces on the board are filled
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))
