# import pygame
WINDOW_HEIGHT = 637
WINDOW_WIDTH = 637
OFFSET = 150
OFFSETRD = 37
BLOCKSIZE = 50
BLACK = '#ffffff00'
GREY = '#A8A8A8'
WHITE = '#ffffff00'
GREEN = '#03823F'
RED = '#ED1C24'
BLUE = '#3E46AF'
YELLOW = '#CCB905'
PURPLE = '#662D91'
CYAN = '#00A99D'
PINK = '#C40580'
BROWN = '#753A0D'
ORANGE = '#F7931E'
colors = [
    GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN,
]
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

colorToLetter = [(c, l)for c, l in zip(colors, letters)]
# SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
