import pygame

FPS = 60
WINDOW_HEIGHT = 635
WINDOW_WIDTH = 635
OFFSET = 150
OFFSET_RIGHT_DOWN = 35
BLOCKSIZE = 50
transparency = 120
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
grid_color = '#FFC4FD'
colors = [
    GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN,
]
letters = ['Ω', '«', '¥', 'ƴ', '¤', 'ǂ', 'Ħ', 'Ʌ']

colorToLetter = list(zip(colors, letters))
assets_dir = 'assets'

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
IMG = pygame.image.load(f'{assets_dir}/board.jpg').convert()
IMG = pygame.transform.smoothscale(IMG, SCREEN.get_size())
SCOREIMG = pygame.image.load(f'{assets_dir}/scoreimg.jpg')
# ['Ω', '♦', '۞', '♫', '☼', '♥', '♠', '♣', 'ƛ']
