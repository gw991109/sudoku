from __future__ import annotations
import pygame
from board import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (100, 200, 100)

# width and height of the window
WINDOW_SIZE = (900, 1000)

# width of walls
WALL = 5
WALL_THICK = 8

pygame.font.init()


class Game:
    """
    A class to represent a game we are currently playing.

    ---Attributes---
    surface: surface to draw on
    board: a Board instance to call methods on and store the actual playing
    board representation, and notes and solutions
    clock: a pygame clock to keep track of time
    time: total time passed
    selected: a tuple representing the position of the currently selected cell
    cell_size: the cell dimension, it is a square so one int is enough
    strikes: the number of strikes the player has gotten
    solved: whether or not the board is solved, used to stop further actions
    on the board once it is solved
    """
    surface: pygame.Surface
    board: Board
    clock: pygame.time.Clock
    time: int
    selected: Tuple(int, int)
    cell_size: int
    strikes: int
    solved: bool

    def __init__(self, board: List[List[int]], surface: pygame.Surface):
        """
        Initialize a game instance.
        :param board: the board which we are playing with, given as a list of
        list of integers, with 0 representing empty cells.
        :param surface: the surface on which we will draw the grid and numbers
        """
        self.surface = surface
        self.board = Board(board)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.selected = None
        self.cell_size = WINDOW_SIZE[0] / 9
        self.strikes = 0
        self.solved = False

    def process_mbdown(self, pos: Tuple[int, int]) -> bool:
        """
        process the mouse action and highlight the selected cell in red.
        :param pos: position of the cell to highlight given in a tuple, format
        should be (x, y)
        :return: true if location is on the surface, false otherwise
        """
        if pos[0] < WINDOW_SIZE[0] and pos[1] < WINDOW_SIZE[1]:
            x = int(pos[0] // self.cell_size)
            y = int(pos[1] // self.cell_size)
            self.selected = (x, y)
            return True
        return False

    def fill_solution(self) -> bool:
        """
        fill the notes at the selected position into the playing board.
        :return: true upon success false otherwise
        """
        if self.selected:
            if self.board.get(self.selected[1], self.selected[0]) == 0:
                if self.board.fill_solution(self.selected[1], self.selected[0]):
                    return True
                self.strikes += 1
                return False
            print("That's filled")
        return False

    def clear(self) -> None:
        """
        set the selected cell to be 0 on the playing board.
        :return: None
        """
        if self.selected:
            self.board.clear(self.selected[1], self.selected[0])

    def visual_solve(self) -> bool:
        """
        Visualize the solving process, correct cells will be outlined in green,
        false or currently visiting cells are outlined in red.
        :return: true on success false otherwise
        """
        # backtrack from the empty slot and try every number
        candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # we have an empty slot
        pos = self.board.find_empty()
        if pos[0] == -1:
            if self.board.check_win():
                return True
            else:
                return False
        else:
            for item in candidates:
                self.draw_outline((pos[1], pos[0]), RED)
                pygame.display.update()
                pygame.time.delay(10)
                if self.board.fill(pos[0], pos[1], item):
                    self.draw_outline((pos[1], pos[0]), GREEN)
                    self.clean(pos[1], pos[0])
                    self.draw_number(pos[1], pos[0], item)
                    pygame.display.update()
                    pygame.time.delay(10)
                    if self.visual_solve():
                        return True
                    self.board.clear(pos[0], pos[1])
                    self.clean(pos[1], pos[0])
            return False

    def fill_notes(self, number) -> bool:
        """
        Fill a given number into the currently selected cell as a note
        :param number: number to fill in as a note
        :return: True on success false otherwise
        """
        if self.selected:
            self.board.fill_notes(self.selected[1], self.selected[0], number)
            return True
        return False

    def clear_notes(self) -> None:
        """
        set the selected cell on the notes board to be 0.
        :return: None
        """
        if self.selected:
            self.board.clear_notes(self.selected[1], self.selected[0])

    def clean(self, x: int, y: int) -> None:
        """
        whiteout the cell with given x and y coordinates
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: None
        """
        rect = pygame.Rect(x * self.cell_size + 20, y * self.cell_size + 20,
                           self.cell_size - 40, self.cell_size - 40)
        pygame.draw.rect(self.surface, WHITE, rect)

    def draw_grid(self) -> None:
        """
        draw the 9x9 grid onto our surface
        :return: None
        """
        self.surface.fill(WHITE)
        for i in range(10):
            if i % 3 == 0:
                thickness = 5
            else:
                thickness = 1
            # draw horizontal line
            pygame.draw.line(self.surface, BLACK,
                             (0, self.cell_size * i),
                             (WINDOW_SIZE[0], self.cell_size * i),
                             thickness)
            # draw vertical line
            pygame.draw.line(self.surface, BLACK,
                             (self.cell_size * i, 0),
                             (self.cell_size * i, WINDOW_SIZE[0],),
                             thickness)

    def draw_outline(self, pos: Tuple[int, int],
                     color: Tuple[int, int, int]) -> None:
        """
        Outline a given cell with a given color.
        :param pos: position of the cell given in a tuple
        :param color: color to outline with
        :return: None
        """
        rect = pygame.Rect(pos[0] * self.cell_size, pos[1] * self.cell_size,
                           self.cell_size, self.cell_size)
        pygame.draw.rect(self.surface, color, rect, 5)

    def draw_number(self, x: int, y: int, number) -> None:
        """
        Draw a given number into a given cell
        :param x: x position of the cell
        :param y: y position of the cell
        :param number: number to draw
        :return: None
        """
        font = pygame.font.SysFont('calibri', 50)
        text_surface = font.render(str(number), True, BLACK)
        self.surface.blit(text_surface,
                          ((x + 0.4) * self.cell_size,
                           (y + 0.35) * self.cell_size))

    def draw_numbers(self) -> None:
        """
        Draw all numbers in our playing board onto the surface
        :return: None
        """
        board = self.board.get_board()
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    font = pygame.font.SysFont('calibri', 50)
                    text_surface = font.render(str(board[row][col]),
                                               True, BLACK)
                    self.surface.blit(text_surface,
                                      ((col + 0.4) * self.cell_size,
                                       (row + 0.35) * self.cell_size))

    def draw_notes(self) -> None:
        """
        Draw all numbers in our notes onto the surface, in light green
        :return: None
        """
        notes = self.board.get_notes()
        for row in range(9):
            for col in range(9):
                if notes[row][col] != 0:
                    font = pygame.font.SysFont('calibri', 50)
                    text_surface = font.render(str(notes[row][col]),
                                               True, LIGHT_GREEN)
                    self.surface.blit(text_surface,
                                      ((col + 0.4) * self.cell_size,
                                       (row + 0.35) * self.cell_size))

    def draw_time(self) -> None:
        """
        Draw the time spent so far in this game, in hours:minutes:seconds
        :return: None
        """
        self.clock.tick()
        if not self.solved:
            self.time += self.clock.get_time()
        seconds_total = self.time // 1000
        seconds = seconds_total % 60
        minutes_total = seconds_total // 60
        minutes = minutes_total % 60
        hours = minutes_total // 60
        font_text = pygame.font.SysFont('calibri', 40)
        text_surface = font_text.render("Time Passed:", True, BLACK)
        font_num = pygame.font.SysFont('calibri', 40)
        num_surface = font_num.render(
            "{}:{}:{}".format(hours, minutes, seconds), True, BLACK)

        self.surface.blit(text_surface, (20, 920))
        self.surface.blit(num_surface, (20, 960))

    def draw_strikes(self) -> None:
        """
        Draw how many strikes have we had in this game so far
        :return: None
        """
        string = ''
        for i in range(self.strikes):
            string += 'X '
        font_text = pygame.font.SysFont('calibri', 40)
        text_surface = font_text.render("Strikes:", True, BLACK)
        font_x = pygame.font.SysFont('calibri', 40)
        x_surface = font_x.render(string, True, RED)

        self.surface.blit(text_surface, (600, 920))
        self.surface.blit(x_surface, (600, 960))


def main():
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("SUDOKU")
    board = [[6, 0, 2, 3, 8, 0, 0, 0, 4],
             [4, 0, 5, 0, 7, 0, 0, 9, 0],
             [0, 0, 3, 0, 5, 0, 0, 0, 0],
             [5, 0, 0, 8, 9, 0, 0, 2, 0],
             [2, 4, 9, 0, 0, 0, 5, 8, 7],
             [0, 3, 0, 0, 2, 4, 0, 0, 1],
             [0, 0, 0, 0, 4, 0, 6, 0, 0],
             [0, 9, 0, 0, 1, 0, 7, 0, 8],
             [8, 0, 0, 0, 3, 6, 2, 0, 9]]
    game = Game(board, surface)

    running = True
    key = None

    while running:
        game.draw_grid()
        if not game.solved:
            game.draw_notes()
        game.draw_numbers()
        game.draw_time()
        game.draw_strikes()

        if game.selected:
            game.draw_outline(game.selected, RED)

        pygame.display.update()

        if game.strikes == 3:
            running = False
            print("Game over")
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.process_mbdown(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if key:
                    game.fill_notes(key)
                if event.key == pygame.K_DELETE:
                    game.clear_notes()
                if event.key == pygame.K_SPACE:
                    if game.visual_solve():
                        game.solved = True
                if event.key == pygame.K_RETURN:
                    game.fill_solution()
            key = None

    pygame.quit()


if __name__ == '__main__':
    main()
