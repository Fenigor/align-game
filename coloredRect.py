import pygame

BLOCKSIZE = 50


class ColoredRect(pygame.Rect):
    def __init__(self, color, x, y):
        super().__init__(x, y, BLOCKSIZE, BLOCKSIZE)
        x = (x - 150) / 50
        y = (y - 150) / 50
        self.color = color
        self.grid_x = int(x)
        self.grid_y = int(y)

    def __str__(self):
        return f'{super().__str__()}, {self.color}'

    def __repr__(self):
        return repr(self.__str__())

    def draw_colored_rect(self, color, fill=0, overide=True):
        if overide:
            self.color = color
        pygame.draw.rect(pygame.display.get_surface(), color, self, fill)
        return self

    def draw_text(self, text, font_size=20, color=(0, 0, 0)):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=self.center)
        pygame.display.get_surface().blit(text_surface, text_rect)
        return self
