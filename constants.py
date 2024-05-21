# import pygame
WINDOW_HEIGHT = 635
WINDOW_WIDTH = 635
OFFSET = 150
OFFSETRD = 37
BLOCKSIZE = 50
BLACK = (0, 0, 0, 0)
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
FIELD = '#FFC4FD'
colors = [
    GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN,
]
letters = ['Ω', '«', '¥', 'ƴ', '¤', 'ǂ', 'Ħ', 'Ʌ']

colorToLetter = [(c, l)for c, l in zip(colors, letters)]
# SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# ['Ω', '♦', '۞', '♫', '☼', '♥', '♠', '♣', 'ƛ']
