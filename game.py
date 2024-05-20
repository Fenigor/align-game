import random
from time import sleep

import pygame

from astar import astar
from coloredRect import ColoredRect
from constants import BLACK
from constants import BLOCKSIZE
from constants import colorToLetter
from constants import OFFSET
from constants import OFFSETRD
from constants import WHITE
from constants import WINDOW_HEIGHT
from constants import WINDOW_WIDTH
# from constants import WHITE
# from buttons import Buttons
# from buttons import Buttons
# from stats import Stats


def rand_pair():
    return random.choice(colorToLetter)


def normalize_cords(x, y):
    x = x - (x % BLOCKSIZE)
    y = y - (y % BLOCKSIZE)
    return (x, y)


class AlignIt:
    def __init__(self, dim=9):
        pygame.init()
        self.spawn = True
        self.moves_made = 0
        self.scoreall = 0
        # self.buttons_instance = Buttons(self.scoreall, self.moves_made)
        self.removed_lines = 0
        self.sqr_grid = [
            [
                ColoredRect(x, y, BLACK)
                for x in range(dim)
            ] for y in range(dim)
        ]
        self.space = [[0 for _ in range(dim)] for _ in range(dim)]
        self.next_sqrs = []
        self.selected_square = None
        self.grow = True
        self.move_made = True
        self.same_color_counter = 0
        # self.stats = Stats()

    def setup_game(self, next_pairs):
        global SCREEN, CLOCK
        pygame.init()
        self.text_font = pygame.font.SysFont('Arial', 30)
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        img = pygame.image.load('unnamed.jpg')
        SCREEN.blit(img, (0, 0))
        self.draw_future_grid(next_pairs)
        self.draw_grid(True)

    def aprove_spawning(self, next_pairs):
        for x_grid, y_grid in self.draw_predicted(next_pairs):
            self.update_score(x_grid, y_grid)

    def main(self):
        next_pair = [rand_pair() for _ in range(3)]
        self.setup_game(next_pair)

        while True:
            self.draw_grid(False)
            if self.move_made:
                if self.spawn:
                    self.aprove_spawning(next_pair)
                self.spawn = True
                next_pair = [rand_pair() for _ in range(3)]
                self.draw_future_grid(next_pair)
                self.move_made = False
            self.handle_mouse_click()
            if self.selected_square is not None:
                self.makes_square_pulse()
            # self.stats.score(self.scoreall)
            # self.stats.movesmade()
            pygame.display.update()

    def get_square_cords(self, x, y):
        x, y = normalize_cords(x, y)
        x_grid = int((x / BLOCKSIZE) - 3)
        y_grid = int((y / BLOCKSIZE) - 3)
        return x_grid, y_grid

    def move_square(self, x, y):
        start = (
            self.selected_square.grid_x,
            self.selected_square.grid_y,
        )
        end = (x, y)
        path = astar(self.space, start, end)
        if not path:
            return
        first = path[0]
        last = path[-1]
        self.space[last[0]][last[1]] = 1
        self.space[first[0]][first[1]] = 0
        start_square = self.sqr_grid[first[0]][first[1]]
        color = start_square.color
        letter = start_square.letter
        self.moves_made += 1
        for i, cords in enumerate(path):
            prev_x = path[i-1][0]
            prev_y = path[i-1][1]
            self.sqr_grid[prev_x][prev_y].draw_colored_rect(BLACK)
            x = cords[0]
            y = cords[1]
            self.sqr_grid[x][y].draw_colored_rect(color).draw_text(letter)
            sleep(0.05)
            pygame.display.update()
        self.move_made = True
        self.selected_square = None

    def update_score(self, x_grid, y_grid):
        lines = self.find_adjacent_color(x_grid, y_grid)
        self.check_length_remove_square(lines)

    def handle_mouse_click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (
                    x < OFFSET or y < OFFSET or
                    x >= WINDOW_WIDTH - OFFSETRD or
                    y >= WINDOW_HEIGHT - OFFSETRD
                ):
                    break
                x_grid, y_grid = self.get_square_cords(x, y)
                if self.selected_square and self.space[x_grid][y_grid] == 0:
                    self.move_square(x_grid, y_grid)
                    self.update_score(x_grid, y_grid)
                    break
                if self.space[x_grid][y_grid] == 0:
                    break
                self.selected_square = self.sqr_grid[x_grid][y_grid]
            if event.type == pygame.QUIT:
                pygame.QUIT()

    def makes_square_pulse(self):
        sleep(.5)
        if self.grow:
            inf_val = 2
            self.grow = False
            color = self.selected_square.color

        else:
            inf_val = -2
            self.grow = True
            color = BLACK
        self.selected_square.inflate_ip(inf_val, inf_val)
        self.selected_square.draw_colored_rect(color, 2, False)
        pygame.display.update()

    def draw_grid(self, new):
        if new:
            row = 0
            for row, x in enumerate(
                range(
                    OFFSET, WINDOW_WIDTH - OFFSETRD, BLOCKSIZE,
                ),
            ):
                for col, y in enumerate(
                    range(OFFSET, WINDOW_HEIGHT - OFFSETRD, BLOCKSIZE),
                ):
                    rect = ColoredRect(x, y, WHITE)
                    # have to figure out how to keep the grid but not to draw
                    self.sqr_grid[row][col] = rect

        # else:
        #     for row in self.sqr_grid:
        #         for rect in row:
        #             rect.draw_colored_rect(RED, 1, False)

    def draw_future_grid(self, next_pairs):
        for i, (color, letter) in enumerate(next_pairs):
            self.next_sqrs = ColoredRect(
                BLOCKSIZE,
                ((i + 4.7) * BLOCKSIZE) +
                (i * 41),
                color,
                letter,
            ).draw_colored_rect(
                color,
            ).draw_text(letter)

    def draw_predicted(self, next_pairs):
        placed = 0
        future_sqr_cord = []
        available_positions = 0
        for row in self.space:
            available_positions += row.count(0)
        while (
            placed < 3 and
            available_positions > 0 and
            next_pairs
        ):
            x = random.randint(OFFSET, WINDOW_WIDTH)
            y = random.randint(OFFSET, WINDOW_HEIGHT)
            x_grid, y_grid = self.get_square_cords(x, y)
            if (
                0 <= x_grid < len(self.space[0])
                and 0 <= y_grid < len(self.space[0])
                and self.space[x_grid][y_grid] == 0
            ):
                color, letter = next_pairs.pop()

                self.sqr_grid[x_grid][y_grid] = ColoredRect(
                    OFFSET + x_grid * BLOCKSIZE,
                    OFFSET + y_grid * BLOCKSIZE,
                    color,
                    letter,
                ).draw_colored_rect(
                    color,
                ).draw_text(letter)
                self.space[x_grid][y_grid] = 1
                placed += 1
                future_sqr_cord.append((x_grid, y_grid))
                available_positions -= 1
                self.update_score(x_grid, y_grid)
        if available_positions == 0:
            # self.stats.game_over('Game Over', (RED), 10, 10)
            pass
        return future_sqr_cord

    def find_adjacent_color(self, x, y):
        org_x, org_y = x, y
        directions = [
            (1, 0),  (0, 1), (1, 1), (1, -1),
            (-1, 0),  (0, -1), (-1, -1), (-1, 1),
        ]
        lines = {
            0: [(org_x, org_y)],
            1: [(org_x, org_y)],
            2: [(org_x, org_y)],
            3: [(org_x, org_y)],
        }
        color = self.sqr_grid[org_x][org_y].color
        for i, direction in enumerate(directions):
            x, y = org_x, org_y
            dir_x, dir_y = direction
            while True:
                x += dir_x
                y += dir_y
                try:
                    color_adj = self.sqr_grid[x][y].color
                    is_same_color = color == color_adj
                    is_taken = self.space[x][y] == 1
                    if is_taken and is_same_color:
                        if x < 0 or y < 0:
                            continue
                        lines[i % 4].append((x, y))
                    else:
                        break
                except Exception:
                    break
        return lines

    def check_length_remove_square(self, lines):
        for direction, line in lines.items():
            if len(line) >= 5:
                self.spawn = False
                for x, y in line:
                    self.sqr_grid[x][y].draw_colored_rect(BLACK)
                    self.space[x][y] = 0
                if direction in [0, 1, 2, 3]:
                    self.scoreall += len(line)


if __name__ == '__main__':
    game = AlignIt()
    game.main()
