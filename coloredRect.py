import pygame

from constants import WHITE
# from constants import surface
BLOCKSIZE = 50


class ColoredRect(pygame.Rect):
    def __init__(self, x, y, color, letter=None):
        super().__init__(x, y, BLOCKSIZE, BLOCKSIZE)
        x = (x - 150) / 50
        y = (y - 150) / 50
        self.color = color
        self.grid_x = int(x)
        self.grid_y = int(y)
        self.letter = letter

    def __str__(self):
        return f'{super().__str__()}, {self.color}, {self.letter}'

    def __repr__(self):
        return repr(self.__str__())

    def draw_colored_rect(self, color, fill=0, overwrite=True):
        if overwrite:
            self.color = color
        pygame.draw.rect(pygame.display.get_surface(), color, self, fill)
        return self

    def draw_text(self, letter, font_size=20, color=WHITE):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(letter, True, color)
        text_rect = text_surface.get_rect(center=self.center)
        pygame.display.get_surface().blit(text_surface, text_rect)
        self.letter = letter
        return self
