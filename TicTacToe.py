import pygame as pg
import colours
from enum import Enum


class Cell(Enum):
    """"Class defines statuses of cell 0 - cell is empty, 1 - there is a cross in cell, 2 - there is a zero in cell"""
    VOID = 0
    CROSS = 1
    ZERO = 2


class Player:
    """Class, which contains player's name and type of game-figure"""
    def __init__(self, name, character):
        self.name = name
        self.character = character


class GameField:
    """Class processes game field with given parameters"""
    def __init__(self):
        self.width = 3
        self.height = 3
        self.cells = [[Cell.VOID]*self.height for i in range(self.width)]


class GameFieldView:
    """Class processes interaction between user and field, where game is drawn"""
    def __init__(self, field, cell_size):
        self._cell_size = cell_size
        self._cross = Cell.CROSS
        self._zero = Cell.ZERO
        self._field = field
        self._height = field.height * self._cell_size
        self._width = field.width * self._cell_size

    def is_coords_correct(self, x, y):
        if self._width / 10 < x < self._width + self._width / 10 and self._height / 10 < y < self._height + self._height / 10:
            return True

    def get_cell_clicked(self, x, y):
        cell = []
        if x < self._width / 3 + self._width / 10:
            cell.append(0)
        elif x < 2 * self._width / 3 + self._width / 10:
            cell.append(1)
        else:
            cell.append(2)

        if y < self._height / 3 + self._height / 10:
            cell.append(0)
        elif y < 2 * self._height / 3 + self._height / 10:
            cell.append(1)
        else:
            cell.append(2)

        return cell

    def draw(self, window, colour=colours.green):
        line_width = int(window.get_width() / 150)
        pg.draw.line(window, colour, (self._cell_size + self._width / 10, self._height / 10), (self._cell_size + self._width / 10, self._height + self._height / 10), line_width)
        pg.draw.line(window, colour, (self._width - self._cell_size + self._width / 10, self._height / 10), (self._width - self._cell_size + self._width / 10, self._height + self._height / 10), line_width)
        pg.draw.line(window, colour, (self._width / 10, self._cell_size + self._height / 10), (self._width + self._width / 10, self._cell_size + self._height / 10), line_width)
        pg.draw.line(window, colour, (self._width / 10, self._height - self._cell_size + self._height / 10), (self._width + self. _width / 10, self._height - self._cell_size + self._height / 10), line_width)
        for column in range(self._field.width):
            for cell in range(self._field.height):
                if self._field.cells[column][cell] == Cell.CROSS:
                    pg.draw.line(window, colour, (line_width + self._width / 10 + column * self._cell_size, line_width + self._height / 10 + cell * self._cell_size), (self._width / 10 + column * self._cell_size + self._cell_size - line_width, self._height / 10 + cell * self._cell_size + self._cell_size - line_width), line_width)
                    pg.draw.line(window, colour, (self._width / 10 + self._cell_size * column + line_width, self._height / 10 + self._cell_size + self._cell_size * cell - line_width), (self._width / 10 + self._cell_size + self._cell_size * column - line_width, self._height / 10 + self._cell_size * cell + line_width), line_width)
                elif self._field.cells[column][cell] == Cell.ZERO:
                    pg.draw.ellipse(window, colour, (self._width / 10 + self._cell_size * column + line_width, self._height / 10 + self._cell_size * cell + line_width, self._cell_size - 2 * line_width, self._cell_size - 2 * line_width), line_width)


class GameRoundManager:
    """Class, that controls processes in game"""
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self._current_player = 0
        self.field = GameField()

    def handle_click(self, cell):
        i, j = cell
        field_not_full = False
        if self.field.cells[i][j] == Cell.VOID:
            if self._current_player == 0:
                self.field.cells[i][j] = self.players[self._current_player].character
                self._current_player += 1
            elif self._current_player == 1:
                self.field.cells[i][j] = self.players[self._current_player].character
                self._current_player -= 1
        for column in self.field.cells:
            field_not_full = field_not_full or Cell.VOID in column
        if not field_not_full:
            print("Game Over, it's a game draw!")


class GameWindow:
    """Works with field widget and processes game round"""
    def __init__(self, resolution=(1600, 900), fps=60):
        self._resolution = resolution
        self._fps = fps
        player1 = Player("Player1", Cell.CROSS)
        player2 = Player("Player2", Cell.ZERO)
        self._game_manager = GameRoundManager(player1, player2)
        self._window = pg.display.set_mode(self._resolution)
        self._field_widget = GameFieldView(self._game_manager.field, self._window.get_height()/4)

    def setup(self):
        print(f"Enter name, {self._game_manager.players[0].name}: ")
        self._game_manager.players[0].name = input()
        print(f"Enter name, {self._game_manager.players[1].name}: ")
        self._game_manager.players[1].name = input()
        pg.display.set_caption(f"TicTacToe {self._game_manager.players[0].name} vs {self._game_manager.players[1].name}")

    def main_loop(self):
        is_running = True
        timer = pg.time.Clock()
        while is_running:
            for event in pg.event.get():
                timer.tick(self._fps)
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    is_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    x, y = mouse_pos
                    if self._field_widget.is_coords_correct(x, y):
                        self._game_manager.handle_click(self._field_widget.get_cell_clicked(x, y))
            self._window.fill(colours.white)
            self._field_widget.draw(self._window, colours.rand_colour)
            pg.display.flip()


def main():
    window = GameWindow()
    window.setup()
    window.main_loop()


if __name__ == '__main__':
    main()
