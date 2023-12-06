import pygame as pg
import colours
from enum import Enum


class Cell(Enum):
    """"Class defines statuses of cell VOID - cell is empty, CROSS - there is a cross in cell, ZERO - there is a zero in cell"""
    VOID = 0
    CROSS = 1
    ZERO = 2


class Player:
    """Class, which contains player's name and type of game-figure"""
    def __init__(self, name: str, character: Cell):
        self.name = name
        self.character = character
        self.result = 0


class GameField:
    """Class processes game field with given parameters"""
    def __init__(self):
        self.width = 3
        self.height = 3
        self.cells = [[Cell.VOID]*self.height for i in range(self.width)]

    def new_round(self):
        self.cells = [[Cell.VOID]*self.height for i in range(self.width)]


class GameFieldView:
    """Class processes interaction between user and field, where game is drawn"""
    def __init__(self, field: GameField, cell_size: float):
        self._cell_size = cell_size
        self._field = field
        self._height = field.height * self._cell_size
        self._width = field.width * self._cell_size
        self.start_pos_x = self._width / 10
        self.start_pos_y = self._height / 10

    def is_coords_correct(self, x: float, y: float) -> bool:
        """
        Checks if given coordinates of a click are refer to game field
        :param x: x-coordinate of mouse click
        :param y: y-coordinate of mouse click
        :return: bool
        """
        if self._width / 10 < x < self._width + self._width / 10 and self._height / 10 < y < self._height + self._height / 10:
            return True

    def get_cell_clicked(self, x: float, y: float) -> list:
        """
        Calculates which cell of game field given coordinates refer to and returns it
        :param x: x-coordinate of mouse click
        :param y: y-coordinate of mouse click
        :return: cell, where click was made
        """
        cell = [None, None]
        for i in range(len(self._field.cells)):
            if self.start_pos_x + self._cell_size * i < x < self.start_pos_x + self._cell_size * i + self._cell_size:
                cell[0] = i
        for i in range(len(self._field.cells)):
            if self.start_pos_y + self._cell_size * i < y < self.start_pos_y + self._cell_size * i + self._cell_size:
                cell[1] = i
        return cell

    def draw(self, window, colour: tuple):
        """
        Draws game field and characters on a given surface
        :param window: Surface, where game field and characters should be drawn
        :param colour: Colour of field and characters
        :return:None
        """
        line_width = int(window.get_width() / 150)
        for i in range(len(self._field.cells) - 1):
            pg.draw.line(window, colour, (self.start_pos_x + self._cell_size * i + self._cell_size, self.start_pos_y),
                         (self.start_pos_x + self._cell_size * i + self._cell_size, self._height + self.start_pos_y), line_width)
        for i in range(len(self._field.cells) - 1):
            pg.draw.line(window, colour, (self.start_pos_x, self.start_pos_y + self._cell_size * i + self._cell_size),
                         (self.start_pos_x + self._width, self.start_pos_y + self._cell_size * i + self._cell_size), line_width)
        for column in range(self._field.width):
            for cell in range(self._field.height):
                if self._field.cells[column][cell] == Cell.CROSS:
                    pg.draw.line(window, colour, (self.start_pos_x + column * self._cell_size + line_width, line_width + self.start_pos_y + cell * self._cell_size),
                                 (self.start_pos_x + column * self._cell_size + self._cell_size - line_width, self.start_pos_y + cell * self._cell_size + self._cell_size - line_width), line_width)
                    pg.draw.line(window, colour, (self.start_pos_x + self._cell_size * column + line_width, self.start_pos_y + self._cell_size + self._cell_size * cell - line_width),
                                 (self.start_pos_x + self._cell_size + self._cell_size * column - line_width, self.start_pos_y + self._cell_size * cell + line_width), line_width)
                elif self._field.cells[column][cell] == Cell.ZERO:
                    pg.draw.ellipse(window, colour, (self.start_pos_x + self._cell_size * column + line_width, self.start_pos_y + self._cell_size * cell + line_width, self._cell_size - 2 * line_width, self._cell_size - 2 * line_width), line_width)


class GameRoundManager:
    """Class, that controls processes in game"""
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.current_player = 0
        self.field = GameField()

    def handle_click(self, cell: list):
        """
        Handles click, puts character of a current player in given cell, checks if game field is not full
        :param cell: cell, where click was made
        :return: None
        """
        i, j = cell
        if self.field.cells[i][j] == Cell.VOID:
            if self.current_player == 0:
                self.field.cells[i][j] = self.players[self.current_player].character
                self.current_player += 1
            elif self.current_player == 1:
                self.field.cells[i][j] = self.players[self.current_player].character
                self.current_player -= 1

    def is_game_over(self) -> bool:
        """
        Checks if game is not over
        :return: None
        """
        game_over = False
        for column in range(self.field.height):
            game_over = True
            # Check for three in line crosses or zeros in horizontal lines
            for cell in range(self.field.width - 1):
                if self.field.cells[cell][column] == Cell.CROSS:
                    game_over = game_over and (self.field.cells[cell][column] == self.field.cells[cell+1][column])
                elif self.field.cells[cell][column] == Cell.ZERO:
                    game_over = game_over and (self.field.cells[cell][column] == self.field.cells[cell+1][column])
                else:
                    game_over = False
            if game_over:
                break
            game_over = True
            # Check for three in line crosses or zeros in vertical lines
            for i in range(self.field.width - 1):
                if self.field.cells[column][i] == Cell.CROSS:
                    game_over = game_over and (self.field.cells[column][i] == self.field.cells[column][i+1])
                elif self.field.cells[column][i] == Cell.ZERO:
                    game_over = game_over and (self.field.cells[column][i] == self.field.cells[column][i+1])
                else:
                    game_over = False
            if game_over:
                break
            game_over = True
            # Check for three in line crosses or zeros in primary diagonal
            for j in range(self.field.width - 1):
                if self.field.cells[j][j] == Cell.CROSS:
                    game_over = game_over and (self.field.cells[j][j] == self.field.cells[j+1][j+1])
                elif self.field.cells[j][j] == Cell.ZERO:
                    game_over = game_over and (self.field.cells[j][j] == self.field.cells[j+1][j+1])
                else:
                    game_over = False
            if game_over:
                break
            game_over = True
            # Check for three in line crosses or zeros in secondary diagonal
            j = self.field.width - 1
            for i in range(self.field.width - 1):
                if self.field.cells[i][j] == Cell.CROSS:
                    game_over = game_over and (self.field.cells[i][j] == self.field.cells[i+1][j-1])
                elif self.field.cells[i][j] == Cell.ZERO:
                    game_over = game_over and (self.field.cells[i][j] == self.field.cells[i+1][j-1])
                else:
                    game_over = False
                j -= 1
            if game_over:
                break
        return game_over


class GameWindow:
    """Works with field widget and processes game round. Window should have proportions at least 4 : 3"""
    def __init__(self, resolution=(1600, 900), fps=60):
        self._resolution = resolution
        assert resolution[0] / resolution[1] >= 4 / 3, "Wrong resolution parameters! Resolution should have at least 4 : 3 proportions"
        self._fps = fps
        player1 = Player("Player1", Cell.CROSS)
        player2 = Player("Player2", Cell.ZERO)
        self._game_manager = GameRoundManager(player1, player2)
        self._window = pg.display.set_mode(self._resolution)
        self._field_widget = GameFieldView(self._game_manager.field, self._window.get_height()/(self._game_manager.field.width + 1))

    def setup(self):
        """
        Gets player's names
        :return:
        """
        print(f"Enter name, {self._game_manager.players[0].name}: ")
        self._game_manager.players[0].name = input()
        print(f"Enter name, {self._game_manager.players[1].name}: ")
        self._game_manager.players[1].name = input()
        pg.display.set_caption(f"TicTacToe {self._game_manager.players[0].name} (Crosses) vs {self._game_manager.players[1].name} (Zeros)")

    def show_results(self):
        """
        Shows game result on surface of GameWindow
        :return: None
        """
        pg.font.init()
        field_not_full = False
        font = pg.font.Font(None, int(self._window.get_height() / 20))
        player1 = font.render(self._game_manager.players[0].name, True, colours.rand_colour)
        player2 = font.render(self._game_manager.players[1].name, True, colours.rand_colour)
        result1 = font.render(str(self._game_manager.players[0].result), True, colours.rand_colour)
        result2 = font.render(str(self._game_manager.players[1].result), True, colours.rand_colour)
        game_over = font.render("Game Over", True, colours.rand_colour)
        game_draw = font.render("It's a Game Draw", True, colours.rand_colour)
        game_tip = font.render("Press 'R' to restart", True, colours.rand_colour)
        game_turn = font.render(str(self._game_manager.players[self._game_manager.current_player].name + "'s turn!"), True, colours.rand_colour)
        self._window.blit(player1, (self._window.get_width() * 0.7, self._window.get_height() * 0.1))
        self._window.blit(result1, (self._window.get_width() * 0.9, self._window.get_height() * 0.1))
        self._window.blit(player2, (self._window.get_width() * 0.7, self._window.get_height() * 0.15))
        self._window.blit(result2, (self._window.get_width() * 0.9, self._window.get_height() * 0.15))
        self._window.blit(game_turn, (self._window.get_width() * 0.7, self._window.get_height() * 0.2))
        for column in self._game_manager.field.cells:
            field_not_full = field_not_full or Cell.VOID in column
        if self._game_manager.is_game_over():
            game_winner = font.render(str(self._game_manager.players[not self._game_manager.current_player].name + " WIN!"), True, colours.rand_colour)
            self._window.blit(game_over, (self._window.get_width() * 0.7, self._window.get_height() * 0.3))
            self._window.blit(game_winner, (self._window.get_width() * 0.7, self._window.get_height() * 0.35))
            self._window.blit(game_tip, (self._window.get_width() * 0.7, self._window.get_height() * 0.4))
        elif not field_not_full:
            self._window.blit(game_over, (self._window.get_width() * 0.7, self._window.get_height() * 0.3))
            self._window.blit(game_draw, (self._window.get_width() * 0.7, self._window.get_height() * 0.35))
            self._window.blit(game_tip, (self._window.get_width() * 0.7, self._window.get_height() * 0.4))

    def main_loop(self):
        pg.mixer.init()
        is_running = True
        timer = pg.time.Clock()
        while is_running:
            for event in pg.event.get():
                timer.tick(self._fps)
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    is_running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                    if self._game_manager.is_game_over():
                        self._game_manager.players[not self._game_manager.current_player].result += 1
                    self._game_manager.field.new_round()
                    pg.mixer.Sound("New_round.mp3").play()
                    self._game_manager.current_player = 0
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self._game_manager.is_game_over():
                    mouse_pos = pg.mouse.get_pos()
                    if self._field_widget.is_coords_correct(*mouse_pos):
                        if self._game_manager.current_player == 0:
                            pg.mixer.Sound("Draw_sound_X.mp3").play()
                        elif self._game_manager.current_player == 1:
                            pg.mixer.Sound("Draw_sound.mp3").play()
                        self._game_manager.handle_click(self._field_widget.get_cell_clicked(*mouse_pos))
            self._window.fill(colours.white)
            self._field_widget.draw(self._window, colours.rand_colour)
            self.show_results()
            pg.display.update()


def main():
    window = GameWindow()
    window.setup()
    window.main_loop()


if __name__ == '__main__':
    main()
