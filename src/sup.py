from random import shuffle
import pygame
from class_field import *
from menu import *


# для отладки
from time import sleep



WIDTH = 1000
HEIGHT = 700






screen = pygame.display.set_mode((WIDTH, HEIGHT))
field = None
menu = Menu(screen)

# f.build(4, 2)


# f.show()
print()

# f.show_opened()
# f.mark(2, 8)
# f.open(3, 8)
print()
# f.show_opened()





# game_started = False
# 
# while (not game_started):
#





# Меню
started = False
running = True
game_started = False

while (not game_started):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_started = True
            started = True
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(field.closed, field.marked_bombs)
            # print(f"Нажатие мыши в {event.pos}")
            x, y = event.pos[0], event.pos[1]
            
            if event.button == 1: # Левая кнопка
                if menu.start(y, x):                  # курсор на кнопке
                    game_started = True
    
    x, y = pygame.mouse.get_pos()
    menu.show_pygame(y, x)
    pygame.display.flip()

field = Field(screen, 17, 25, 15)



# --------------------------------------------------------------------------------
# Игра

while (not started):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            started = True
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(field.closed, field.marked_bombs)
            # print(f"Нажатие мыши в {event.pos}")
            x, y = event.pos[0], event.pos[1]
            if event.button == 1: # Левая кнопка
                if (field.on_field(y, x)):
                    started = True
                    field.build_pygame(y, x)
            elif event.button == 3: # Правая кнопка
                if (field.on_field(y, x)):
                    pass
    
    field.show_pygame()
    pygame.display.flip()


last_click = 0
double_click = 300

while (not field.is_finished() and running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(field.closed, field.marked_bombs)
            # print(f"Нажатие мыши в {event.pos}")
            x, y = event.pos[0], event.pos[1]
            if event.button == 1: # Левая кнопка
                current_click = pygame.time.get_ticks()
                if (field.on_field(y, x)):
                    f = field.open_pygame(y, x,
                            current_click - last_click < double_click)
                    if f == 9:
                        field.show_pygame_cells(y, x)
                    elif f == 1:
                        field.show_pygame_cell(y, x)
                    else:
                        field.show_pygame()
                last_click = pygame.time.get_ticks()
                
            elif event.button == 3: # Правая кнопка
                if (field.on_field(y, x)):
                    field.mark_pygame(y, x)
                    field.show_pygame_cell(y, x)
            
            
            
            pygame.display.flip()
        #
    #
#



if running:
    if field.lose:
        my_draw_text(screen, HEIGHT // 2, WIDTH // 2, HEIGHT // 3, RED, "LOSE")
        print("GG")
    else:
        my_draw_text(screen, HEIGHT // 2, WIDTH // 2, HEIGHT // 3, GOLDEN, "WIN")
        print("Win")
else:
    print("Interrupted")


pygame.display.flip()


while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
pygame.quit()


#

