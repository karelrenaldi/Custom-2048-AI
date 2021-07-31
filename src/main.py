import copy
import numpy as np


class Game_2048:
    def __init__(self, board) -> None:
        """
            This board coordinate : X greater to right, Y greater to down.
        """
        self.board = copy.deepcopy(board)
        self.rows = 4
        self.cols = 4
        self.max_depth = 4

    def isEqual(self, board) -> bool:
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.board[i][j] != board[i][j]):
                    return False
        return True

    def calculate_goodness(self) -> float:
        """
            This function use for calculate "how good" current state is.
            This function use (sum of element value / total non-empty slot) as calculate approach.
        """
        total_value = 0
        total_non_empty_slot = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if(self.board[i][j] == 0):
                    continue

                total_non_empty_slot += 1
                total_value += self.board[i][j]

        return total_value / total_non_empty_slot

    def can_move(self, move_direction) -> bool:
        if(move_direction == 'up'):
            for j in range(self.cols):
                not_empty_row_idx = None

                # Find row idx specify with current column that not empty block.
                for i in range(3, -1, -1):
                    if(self.board[i][j] != 0):
                        not_empty_row_idx = i
                        break

                if(not_empty_row_idx != None):
                    for i in range(not_empty_row_idx, 0, -1):
                        # Empty block so can move.
                        if(self.board[i - 1][j] == 0):
                            return True

                        # Can merge.
                        if(self.board[i][j] == self.board[i - 1][j]):
                            return True
            return False

        if(move_direction == 'down'):
            for j in range(self.cols):
                not_empty_row_idx = None

                # Find row idx specify with current column that not empty block.
                for i in range(self.rows):
                    if self.board[i][j] != 0:
                        not_empty_row_idx = i
                        break

                if (not_empty_row_idx != None):
                    for i in range(not_empty_row_idx, self.rows - 1):
                        # Empty block so can move.
                        if self.board[i+1][j] == 0:
                            return True

                        # Can merge.
                        if self.board[i][j] == self.board[i+1][j]:
                            return True
            return False

        if(move_direction == 'right'):
            for i in range(self.rows):
                not_empty_col_idx = None

                for j in range(self.cols):
                    if self.board[i][j] != 0:
                        not_empty_col_idx = j
                        break

                if (not_empty_col_idx != None):
                    for j in range(not_empty_col_idx, self.cols - 1):
                        # Empty block so can move.
                        if self.board[i][j+1] == 0:
                            return True

                        # Can merge.
                        if self.board[i][j] == self.board[i][j+1]:
                            return True

            return False

        if(move_direction == 'left'):
            for i in range(self.rows):
                not_empty_col_idx = None

                for j in range(self.cols - 1, -1, -1):
                    if self.board[i][j] > 0:
                        not_empty_col_idx = j
                        break

                if (not_empty_col_idx != None):
                    for j in range(not_empty_col_idx, 0, -1):
                        # Empty block so can move.
                        if self.board[i][j-1] == 0:
                            return True

                        # Can merge.
                        if self.board[i][j] == self.board[i][j-1]:
                            return True

            return False

    def generate_child(self, isMaximizing):
        childs = []

        if(isMaximizing):
            if(self.can_move("up")):
                childs.append("up")
            if(self.can_move("down")):
                childs.append("down")
            if(self.can_move("left")):
                childs.append("left")
            if(self.can_move("right")):
                childs.append("right")
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    # Still empty
                    if(self.board[i][j] == 0):
                        childs.append((i, j, 2))

        return childs

    def is_terminal(self, isMaximizing) -> bool:
        if(isMaximizing):
            if(self.can_move("up")):
                return False
            if(self.can_move("down")):
                return False
            if(self.can_move("left")):
                return False
            if(self.can_move("right")):
                return False
            return True
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if(self.board[i][j] == 0):
                        return False
            return True

    def is_game_over(self) -> bool:
        return self.is_terminal(True)

    def move(self, move_direction):
        if(move_direction == 'up'):
            for j in range(self.cols):
                current_position = 0
                current_value = 0

                for i in range(self.rows):
                    # Empty block
                    if self.board[i][j] == 0:
                        continue

                    # Not assign value
                    if current_value == 0:
                        current_value = self.board[i][j]

                    # Same value can be merge
                    elif current_value == self.board[i][j]:
                        self.board[current_position][j] = 2*current_value
                        current_position += 1
                        current_value = 0

                    # Not same value, assign new_value
                    else:
                        self.board[current_position][j] = current_value
                        current_position += 1
                        current_value = self.board[i][j]

                # After loop if still a value then change position.
                if current_value != 0:
                    self.board[current_position][j] = current_value
                    current_position += 1

                # Empty all cells.
                for i in range(current_position, 4):
                    self.board[i][j] = 0

        if(move_direction == 'down'):
            for j in range(self.cols):
                current_position = 3
                current_value = 0
                for i in range(self.rows - 1, -1, -1):
                    # Empty block
                    if self.board[i][j] == 0:
                        continue

                     # Not assign value
                    if current_value == 0:
                        current_value = self.board[i][j]

                     # Same value can be merge
                    elif current_value == self.board[i][j]:
                        self.board[current_position][j] = 2*current_value
                        current_position -= 1
                        current_value = 0

                     # Not same value, assign new_value
                    else:
                        self.board[current_position][j] = current_value
                        current_position -= 1
                        current_value = self.board[i][j]

                # After loop if still a value then change position.
                if current_value != 0:
                    self.board[current_position][j] = current_value
                    current_position -= 1

                # Empty all cells.
                for i in range(current_position+1):
                    self.board[i][j] = 0

        if(move_direction == 'left'):
            for i in range(self.rows):
                current_position = 0
                current_value = 0
                for j in range(self.cols):
                    # Empty block
                    if self.board[i][j] == 0:
                        continue

                     # Not assign value
                    if current_value == 0:
                        current_value = self.board[i][j]

                    # Same value can be merge
                    elif current_value == self.board[i][j]:
                        self.board[i][current_position] = 2*current_value
                        current_position += 1
                        current_value = 0

                    # Not same value, assign new_value
                    else:
                        self.board[i][current_position] = current_value
                        current_position += 1
                        current_value = self.board[i][j]

                # After loop if still a value then change position.
                if current_value != 0:
                    self.board[i][current_position] = current_value
                    current_position += 1

                # Empty all cells.
                for j in range(current_position, 4):
                    self.board[i][j] = 0

        if(move_direction == 'right'):
            for i in range(self.rows):
                current_position = 3
                current_value = 0
                for j in range(self.cols - 1, -1, -1):
                    # Empty block
                    if self.board[i][j] == 0:
                        continue

                    # Not assign value
                    if current_value == 0:
                        current_value = self.board[i][j]

                    # Same value can be merge
                    elif current_value == self.board[i][j]:
                        self.board[i][current_position] = 2*current_value
                        current_position -= 1
                        current_value = 0

                    # Not same value, assign new_value
                    else:
                        self.board[i][current_position] = current_value
                        current_position -= 1
                        current_value = self.board[i][j]

                 # After loop if still a value then change position.
                if current_value != 0:
                    self.board[i][current_position] = current_value
                    current_position -= 1

                 # Empty all cells.
                for j in range(current_position+1):
                    self.board[i][j] = 0

    def minimax(self, isMaximizing, depth):
        if(isMaximizing):
            best_score = float('-inf')

            if(depth == 0) or self.is_terminal(True):
                return self.calculate_goodness()

            for child in self.generate_child(True):
                dummy_game = Game_2048(self.board)
                dummy_game.move(child)
                score = dummy_game.minimax(False, depth - 1)
                if score > best_score:
                    best_score = score

            return best_score
        else:
            best_score = float('inf')

            if(depth == 0) or self.is_terminal(False):
                return self.calculate_goodness()

            for child in self.generate_child(False):
                dummy_game = Game_2048(self.board)
                dummy_game.board[child[0]][child[1]] = child[2]
                score = dummy_game.minimax(True, depth - 1)
                if score < best_score:
                    best_score = score

            return best_score

    def ai_move(self):
        best_move = 'up'
        best_score = 0
        moves = ['up', 'down', 'left', 'right']

        for move in moves:
            if(self.can_move(move)):
                dummy_game = Game_2048(self.board)
                dummy_game.move(move)
                score = dummy_game.minimax(False, self.max_depth)
                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move


def main():
    board = np.array([
        [32, 4, 2, 4],
        [0, 0, 64, 32],
        [0, 0, 8, 2],
        [2, 0, 0, 2]
    ])

    game = Game_2048(board)
    while(True):
        prev_board = copy.deepcopy(game.board)
        game.move(game.ai_move())
        print(prev_board)
        print()
        print(game.board)

        isFound = False
        row_idx = 0
        col_idx = 0
        for i in range(game.rows):
            for j in range(game.cols):
                if(game.board[i][j] == 0):
                    row_idx = i
                    col_idx = j
                    isFound = True
                    break
            if(isFound):
                break

        if(not(isFound)):
            print("LOSE")
            break
        else:
            game.board[row_idx][col_idx] = 2


main()
