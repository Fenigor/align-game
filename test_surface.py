import sys

import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load and scale the background image
background = pygame.image.load('assets/board.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Square matrix dimensions
rows, cols = 10, 10
square_size = 50
matrix = [[(j * square_size, i * square_size)
           for j in range(cols)] for i in range(rows)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# State matrix to store the color of each square
square_colors = [[None for _ in range(cols)] for _ in range(rows)]


def draw_grid():
    for row in matrix:
        for square in row:
            pygame.draw.rect(
                screen, WHITE, (*square, square_size, square_size), 1,
            )


def draw_squares():
    for i in range(rows):
        for j in range(cols):
            color = square_colors[i][j]
            if color:
                x, y = matrix[i][j]
                pygame.draw.rect(
                    screen, color, (x, y, square_size, square_size),
                )


def draw_inside_square(row, col, color):
    x, y = matrix[row][col]
    # Update the state matrix
    if square_colors[row][col] == color:
        # Clear the square if it's already the specified color
        square_colors[row][col] = None
    else:
        square_colors[row][col] = color


# Initial drawing
screen.blit(background, (0, 0))
draw_grid()
# pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // square_size, x // square_size
            if 0 <= row < rows and 0 <= col < cols:
                draw_inside_square(row, col, RED)

    # Redraw background and grid
    screen.blit(background, (0, 0))
    draw_squares()
    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()
