# puzzle.py
import random
import copy

GOAL_STATE = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

class Puzzle:
    def __init__(self):
        self.board = copy.deepcopy(GOAL_STATE)
        self.shuffle_board()

    def shuffle_board(self):
        flat = [i for i in range(9)]
        random.shuffle(flat)
        self.board = [flat[i*3:(i+1)*3] for i in range(3)]
        while not self.is_solvable() or self.board == GOAL_STATE:
            random.shuffle(flat)
            self.board = [flat[i*3:(i+1)*3] for i in range(3)]

    def is_solvable(self):
        flat = sum(self.board, [])
        inv_count = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                    inv_count += 1
        return inv_count % 2 == 0

    def move_tile(self, row, col):
        empty_row, empty_col = self.find_empty()
        if abs(empty_row - row) + abs(empty_col - col) == 1:
            self.board[empty_row][empty_col], self.board[row][col] = self.board[row][col], self.board[empty_row][empty_col]

    def find_empty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def get_board(self):
        return [row[:] for row in self.board]

    def set_board(self, new_board):
        self.board = [row[:] for row in new_board]

    def is_goal(self):
        return self.board == GOAL_STATE

    def board_to_tuple(self):
        return tuple(tuple(row) for row in self.board)
