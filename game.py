import random
from time import sleep

import pygame

from astar import astar
from coloredRect import ColoredRect
from constants import BLACK
from constants import BLOCKSIZE
from constants import CLOCK
from constants import colorToLetter
from constants import FPS
from constants import grid_color
from constants import IMG
from constants import OFFSET
from constants import OFFSET_RIGHT_DOWN
from constants import SCOREIMG
from constants import SCREEN
from constants import WHITE
from constants import WINDOW_HEIGHT
from constants import WINDOW_WIDTH


def random_color_letter_pair():
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
        self.removed_lines = 0
        self.sqr_grid = [
            [
                ColoredRect(
                    x * BLOCKSIZE + OFFSET, y *
                    BLOCKSIZE + OFFSET, BLACK,
                )
                for x in range(dim)
            ] for y in range(dim)
        ]
        for row, x in enumerate(
                range(
                    OFFSET, WINDOW_WIDTH - OFFSET_RIGHT_DOWN, BLOCKSIZE,
                ),
        ):
            for col, y in enumerate(
                range(
                    OFFSET, WINDOW_HEIGHT -
                    OFFSET_RIGHT_DOWN, BLOCKSIZE,
                ),
            ):
                rect = ColoredRect(x, y, WHITE)
                self.sqr_grid[row][col] = rect.draw_colored_rect(
                    grid_color, 1, False,
                )
        self.space = [[0 for _ in range(dim)] for _ in range(dim)]
        self.next_sqrs = []
        self.selected_square = None
        self.grow = True
        self.move_made = True
        self.same_color_counter = 0
        self.run = True

    def setup_game(self, next_pairs):
        pygame.init()
        self.text_font = pygame.font.SysFont('Arial', 30)
        SCREEN.blit(IMG, (0, 0))
        self.draw_future_grid(next_pairs)
        # self.draw_grid(True)

    def aprove_spawning(self, next_pairs):
        for x_grid, y_grid in self.draw_predicted(next_pairs):
            self.update_score(x_grid, y_grid)

    def score(self):
        formatted_score = f'{self.scoreall:04}'
        x_start = 413
        y_start = 50
        digit_spacing = 35
        score_bg_rect = SCOREIMG.get_rect(topleft=(402, 41))
        SCREEN.blit(SCOREIMG, score_bg_rect)
        for i, digit in enumerate(formatted_score):
            digit_img = self.text_font.render(digit, True, WHITE)
            SCREEN.blit(digit_img, (x_start + i * digit_spacing, y_start))

    def main(self):
        next_pair = [random_color_letter_pair() for _ in range(3)]
        self.setup_game(next_pair)

        while self.run:
            CLOCK.tick(FPS)
            SCREEN.blit(IMG, (0, 0))
            self.draw_squares()
            self.draw_grid(False)
            if self.move_made:
                if self.spawn:
                    self.aprove_spawning(next_pair)
                self.spawn = True
                next_pair = [random_color_letter_pair() for _ in range(3)]
                self.draw_future_grid(next_pair)
                self.move_made = False
            self.handle_mouse_click()
            if self.selected_square is not None:
                self.makes_square_pulse()
            self.score()

            # self.stats.movesmade()
            # SCREEN.blit(IMG, (0, 0))

            pygame.display.update()

        pygame.quit()

    def get_square_cords(self, x, y):
        x, y = normalize_cords(x, y)
        x_grid = int((x / BLOCKSIZE) - 3)
        y_grid = int((y / BLOCKSIZE) - 3)
        return x_grid, y_grid

    def draw_squares(self):
        for i in range(9):
            for j in range(9):
                color = self.sqr_grid[i][j].color
                if color is not BLACK:
                    self.sqr_grid[i][j].draw_colored_rect(color)

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
            sleep(0.1)
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
                    x >= WINDOW_WIDTH - OFFSET_RIGHT_DOWN or
                    y >= WINDOW_HEIGHT - OFFSET_RIGHT_DOWN
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
                self.run = False

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
                    OFFSET, WINDOW_WIDTH - OFFSET_RIGHT_DOWN, BLOCKSIZE,
                ),
            ):
                for col, y in enumerate(
                    range(
                        OFFSET, WINDOW_HEIGHT -
                        OFFSET_RIGHT_DOWN, BLOCKSIZE,
                    ),
                ):
                    rect = ColoredRect(x, y, WHITE)
                    self.sqr_grid[row][col] = rect.draw_colored_rect(
                        grid_color, 1, False,
                    )
        else:
            for row in self.sqr_grid:
                for rect in row:
                    rect.draw_colored_rect(WHITE, 1, False)

    def draw_future_grid(self, next_pairs):
        for i, (color, letter) in enumerate(next_pairs):
            self.next_sqrs = ColoredRect(
                47,
                ((i + 4.67) * BLOCKSIZE) +
                (i * 42),
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
                    self.sqr_grid[x][y].draw_colored_rect(grid_color)
                    self.space[x][y] = 0
                if direction in [0, 1, 2, 3]:
                    self.scoreall += len(line)


if __name__ == '__main__':
    game = AlignIt()
    game.main()
