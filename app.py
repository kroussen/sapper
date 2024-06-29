import random
from typing import List


class Cell:
    """Представляет собой ячейку на игровом поле "Сапер".

    Атрибуты:
        around_mines (int): Количество мин в соседних ячейках.
        mine (bool): Содержит ли ячейка мину.
        fl_open (bool): Открыта ли ячейка.
    """

    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        """Инициализирует ячейку с заданным количеством мин вокруг и флагом наличия мины."""
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.fl_open: bool = False

    def open(self) -> None:
        """Открывает ячейку."""
        self.fl_open = True

    def place_mine(self) -> None:
        """Размещает мину в ячейке."""
        self.mine = True

    def has_mine(self) -> bool:
        """Проверяет, содержится ли в ячейке мина."""
        return self.mine

    def is_open(self) -> bool:
        """Возвращает статус ячейки (открыта ли она)."""
        return self.fl_open

    def get_around_mines(self) -> int:
        """Возвращает количество мин вокруг данной ячейки."""
        return self.around_mines

    def set_adjacent_mines(self, count: int) -> None:
        """Устанавливает количество мин в соседних ячейках."""
        self.around_mines = count


class GamePole:
    """Класс представляет игровое поле для игры "Сапер".

    Атрибуты:
        size (int): Размер игрового поля.
        mines (int): Количество мин на поле.
        board (List[List[Cell]]): Двумерный список, представляющий игровое поле с ячейками.
    """

    def __init__(self, size: int, mines: int) -> None:
        """Инициализирует игровое поле заданного размера с указанным количеством мин."""
        self.size: int = size
        self.mines: int = mines
        self.board: List[List[Cell]] = []

    def init(self) -> None:
        """Инициализация поля: создает ячейки и размещает мины."""
        self.board = [[Cell() for _ in range(self.size)] for _ in range(self.size)]
        self.place_mines()

    def place_mines(self) -> None:
        """Размещает мины на поле в случайных ячейках."""
        mines_placed: int = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if not self.board[row][col].mine:
                self.board[row][col].place_mine()
                mines_placed += 1

    def get_around_mines_count(self, row: int, col: int) -> int:
        """Вычисляет количество мин вокруг указанной ячейки."""
        adjacent_count: int = 0
        for r in range(max(0, row - 1), min(row + 2, self.size)):
            for c in range(max(0, col - 1), min(col + 2, self.size)):
                if (r != row or c != col) and self.board[r][c].mine:
                    adjacent_count += 1
        return adjacent_count

    def get_cell(self, row: int, col: int) -> Cell:
        """Возвращает ячейку по заданным координатам."""
        return self.board[row][col]

    def open_cell(self, row: int, col: int) -> None:
        """Открывает ячейку и, если вокруг нет мин, открывает соседние ячейки."""
        cell: Cell = self.get_cell(row, col)
        if not cell.fl_open:
            cell.open()
            if not cell.has_mine():
                if self.get_around_mines_count(row, col) == 0:
                    for r in range(max(0, row - 1), min(row + 2, self.size)):
                        for c in range(max(0, col - 1), min(col + 2, self.size)):
                            if (r != row or c != col):
                                self.open_cell(r, c)

    def show(self) -> None:
        """Отображает текущее состояние игрового поля."""
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

    def is_game_over(self) -> bool:
        """Проверяет, закончилась ли игра (все ячейки открыты или мина взорвана)."""
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if cell.mine and cell.fl_open:
                    return True
                if not cell.mine and not cell.fl_open:
                    return False
        return True


pole_game = GamePole(10, 12)
pole_game.init()
