import pygame

pygame.init()


def my_draw_text(screen, center_h, center_w, text_h, colour, text):
    font = pygame.font.SysFont(None, text_h)  # шрифт, размер
    
    text_surface = font.render(text, True, colour)
    text_surface.set_alpha(150)
    
    text_rect = text_surface.get_rect()

    text_rect.center = (center_w, center_h)
    
    screen.blit(text_surface, text_rect)



class Button:
    def __init__(self, screen, center_h, center_w, button_h, button_w, text_colour, button_colour, text):
        self.screen = screen
        self.center_h = center_h
        self.center_w = center_w
        self.button_h = button_h
        self.button_w = button_w
        self.text_colour = text_colour
        self.button_colour = button_colour
        self.text = text
        # pressed, pointed
    
    
    def hovered(self, y, x):
        if self.center_w - self.button_w // 2 <= x <= self.center_w + self.button_w // 2:
            if self.center_h - self.button_h // 2 <= y <= self.center_h + self.button_h // 2:
                return True
        return False
    
    
    def show(self, y, x):
        button_h = self.button_h
        button_w = self.button_w
        center_h = self.center_h
        center_w = self.center_w
        if self.hovered(y, x):
            button_h += button_h // 20
            button_w += button_w // 20
        
        
        pygame.draw.rect(self.screen, self.button_colour,
                             (center_w - button_w // 2, center_h - button_h // 2,
                              button_w, button_h))
        
        font = pygame.font.SysFont(None, button_h)  # шрифт, размер
        
        text_surface = font.render(self.text, True, self.text_colour)
        
        text_rect = text_surface.get_rect()

        text_rect.center = (center_w, center_h)
        
        self.screen.blit(text_surface, text_rect)
        
        pygame.draw.rect(self.screen, self.text_colour,
                             (center_w - button_w // 2, center_h - button_h // 2,
                              button_w, button_h), 1)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.HEIGHT, self.WIDTH = screen.get_height(), screen.get_width()
        self.play_button = Button(screen, self.HEIGHT * 2 // 7, self.WIDTH // 2, self.HEIGHT // 12, self.WIDTH // 4,
                   BLACK, LIGHTEST_GRAY, "Играть")
        # difficult_buttons, field_size_buttons
        
    
    
    def draw_text(self, center_h, center_w,
                  text_h, colour, text):
        
        font = pygame.font.SysFont(None, text_h)  # шрифт, размер
        
        text_surface = font.render(text, True, colour)
        
        text_rect = text_surface.get_rect()

        text_rect.center = (center_w, center_h)
        
        self.screen.blit(text_surface, text_rect)
        # координаты левого верхнего угла от text_rect
    
    def show_buttons(self, y, x):
        self.play_button.show(y, x)
    
    def show_pygame(self, y, x):    # (y, x) указателя мыши
        self.screen.fill(WHITE)
        self.draw_text(self.HEIGHT // 8, self.WIDTH // 2,
                       self.HEIGHT // 5, BLACK, "Меню")
        self.show_buttons(y, x)
    
    
    def start(self, y, x):
        return self.play_button.hovered(y, x)


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
