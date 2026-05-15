import pygame

pygame.init()


BLACK = (0, 0, 0)
LIGHTEST_GRAY = (250, 250, 250)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

GREEN_DARKEST = (30, 90, 0)
GREEN = (50, 150, 0)
GREEN_DARK = (40, 120, 0)
GREEN_EMERALD = (0, 255, 0)

BROWN = (120, 80, 0)
BROWN_GRAY = (120, 80, 40)  #(180, 120, 0)

RED = (255, 0, 0)

YELLOW_LIGHT = (255, 255, 150)
YELLOW = (255, 255, 0)
GOLDEN = (255, 215, 0)

BLUE = (0, 0, 255)


def draw_text(screen, center_h, center_w, text_h, colour, text, alpha=None):
    font = pygame.font.SysFont(None, text_h)  # шрифт, размер

    text_surface = font.render(text, True, colour)
    if alpha is not None:
        text_surface.set_alpha(150)

    text_rect = text_surface.get_rect()

    text_rect.center = (center_w, center_h)

    screen.blit(text_surface, text_rect)
