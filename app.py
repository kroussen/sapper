import random


class Cell:

    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

    def open(self):
        self.fl_open = True

    def place_mine(self):
        self.mine = True

    def has_mine(self):
        return self.mine

    def is_open(self):
        return self.fl_open

    def get_around_mines(self):
        return self.around_mines

    def set_adjacent_mines(self, count):
        self.around_mines = count


class GamePole:

    def __init__(self, size, mines):
        self.size = size
        self.mines = mines
        self.board = []

    def init(self):
        self.board = [[Cell() for _ in range(self.size)] for _ in range(self.size)]
        self.place_mines()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(1, self.size - 1)
            col = random.randint(1, self.size - 1)

            if not self.board[row][col].mine:
                self.board[row][col].mine = True
                mines_placed += 1

    def get_around_mines_count(self, row, col):
        adjacent_count = 0
        for r in range(max(0, row - 1), min(row + 2, self.size)):
            for c in range(max(0, col - 1), min(col + 2, self.size)):
                if (r != row or c != col) and self.board[r][c].mine:
                    adjacent_count += 1
        return adjacent_count

    def get_cell(self, row, col):
        return self.board[row][col]

    def open_cell(self, row, col):
        self.board[row][col].open()

    def show(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if cell.fl_open:
                    if cell.mine:
                        print("*", end=" ")
                    else:
                        count = self.get_around_mines_count(row, col)
                        print(count, end=" ")
                else:
                    print("#", end=" ")
            print()

    def is_game_over(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if cell.mine and cell.fl_open:
                    return True
                if not cell.mine and not cell.fl_open:
                    return False
        return True


pole_game = GamePole(10, 12)
