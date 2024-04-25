import random
import sys
from time import sleep

import pygame

from astar import astar
from coloredRect import ColoredRect

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
OFFSET = 150
BLOCKSIZE = 50
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (200, 200, 200)
GREEN = '#00A14B'
RED = '#ED1C24'
BLUE = '#21409A'
YELLOW = '#FFDE17'
PURPLE = '#7F3F98'
CYAN = '#009599'
PINK = (255, 153, 255)
BROWN = (255, 128, 0)
ORANGE = '#F26522'
colors = [GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN]


def rand_color():
    return random.choice(colors)


def normalize_cords(x, y):
    x = x - (x % BLOCKSIZE)
    y = y - (y % BLOCKSIZE)
    return (x, y)


class AlignIt:
    dim = 9

    def __init__(self):
        self.sqr_grid = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.space = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.next_sqrs = []
        self.score = 0
        self.main()

    def setup_game(self, next_colors):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )
        pygame.display.set_caption('Align it!')
        CLOCK = pygame.time.Clock()
        SCREEN.fill(BLACK)
        self.draw_grid(True)
        self.draw_future_grid(next_colors)

    def handle_mouse_click(self, selected_square, next_colors):

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x < OFFSET or y < OFFSET:
                    break
                x, y = normalize_cords(x, y)
                x_grid = int((x / BLOCKSIZE) - 3)
                y_grid = int((y / BLOCKSIZE) - 3)
                if selected_square and self.space[x_grid][y_grid] == 0:
                    start = (selected_square.grid_x, selected_square.grid_y)
                    end = (x_grid, y_grid)
                    path = astar(self.space, start, end)
                    if path is None:
                        break
                    first = path[0]
                    last = path[-1]
                    color = self.sqr_grid[first[0]][first[1]].color
                    self.space[last[0]][last[1]] = 1
                    self.space[first[0]][first[1]] = 0
                    self.move_square(path, color)
                    self.move_made = True
                    selected_square = None
                    self.spawn_blocks(next_colors, 3)
                    break
                if self.space[x_grid][y_grid] == 0:
                    break
                selected_square = self.sqr_grid[x_grid][y_grid]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return selected_square

    def handle_selected_square(self, selected_square, grow):
        if selected_square:
            if grow:
                inf_val = 2
                grow = False
                color = selected_square.color
                sleep(.2)
            else:
                inf_val = -2
                grow = True
                color = WHITE
                sleep(.5)
            selected_square.inflate_ip(inf_val, inf_val)
            selected_square.draw_colored_rect(color, 2, False)
            return grow

    def main(self):
        next_colors = [rand_color() for _ in range(3)]
        self.setup_game(next_colors)
        move_made = True
        selected_square = None
        grow = True

        while True:
            self.draw_grid(False)
            if move_made:
                self.spawn_blocks(next_colors, 3)
                next_colors = [rand_color() for _ in range(3)]
                self.draw_future_grid(next_colors)
                move_made = False
            selected_square = self.handle_mouse_click(
                selected_square, next_colors,
            )
            grow = self.handle_selected_square(selected_square, grow)
            pygame.display.update()

    def move_square(self, path, color):
        for i, cords in enumerate(path):
            prev_x = path[i-1][0]
            prev_y = path[i-1][1]
            self.sqr_grid[prev_x][prev_y].draw_colored_rect(BLACK)
            x = cords[0]
            y = cords[1]
            self.sqr_grid[x][y].draw_colored_rect(color)
            sleep(0.1)
            pygame.display.update()

    def draw_grid(self, new):
        if new:
            row = 0
            for x in range(OFFSET, WINDOW_WIDTH, BLOCKSIZE):
                col = 0
                for y in range(OFFSET, WINDOW_HEIGHT, BLOCKSIZE):
                    rect = ColoredRect(WHITE, x, y)
                    self.sqr_grid[row][col] = rect.draw_colored_rect(
                        WHITE, 1, False,
                    )
                    col += 1
                row += 1
        else:
            for row in self.sqr_grid:
                for rect in row:
                    rect.draw_colored_rect(WHITE, 1, False)

    def draw_future_grid(self, colors):
        self.next_sqrs.clear()
        for i in range(3):
            if i < len(colors):
                color = colors[i]
            else:
                color = rand_color()

            rect = ColoredRect(
                color,
                BLOCKSIZE,
                ((i + 5) * BLOCKSIZE) + (i * 25),
            ).draw_colored_rect(color)
            self.next_sqrs.append(rect)

    def spawn_blocks(self, next_colors, num_blocks):
        for color in next_colors[:num_blocks]:
            while True:
                x = random.randint(OFFSET, WINDOW_WIDTH - BLOCKSIZE)
                y = random.randint(OFFSET, WINDOW_HEIGHT - BLOCKSIZE)
                print(' x   y', x, y)
                x, y = normalize_cords(x, y)
                x_grid = int((x / BLOCKSIZE) - 3)
                y_grid = int((y / BLOCKSIZE) - 3)
                print('x_grid y_grid', x_grid, y_grid)
                if (
                    0 <= x_grid < len(self.space[0])
                    and 0 <= y_grid < len(self.space[0])

                    and self.space[x_grid][y_grid] == 0
                ):
                    print('block can spawn x_grid y_grid')
                    self.sqr_grid[x_grid][y_grid] = ColoredRect(
                        color,
                        x,
                        y,
                    ).draw_colored_rect(color)
                    self.space[x_grid][y_grid] = 1
                    break
                else:
                    print('block cannot spawn!!!!!!!!!!!!!!')


if __name__ == '__main__':
    AlignIt()
