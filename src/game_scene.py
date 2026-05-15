import pygame
from field_view import FieldView
from utils import draw_text, RED, GOLDEN


DOUBLE_CLICK_INTERVAL = 300

class GameScene:
    def __init__(self, screen, height, width, percent):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.field = FieldView(self.screen, height, width, percent)
        self.should_quit = False

    def run(self):
        self.run_stage_start()
        self.run_stage_first_click()
        if self.should_quit:
            return
        self.run_stage_next_clicks()
        if self.should_quit:
            return
        self.run_stage_game_over()

    def run_stage_start(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.field.show_pygame()
        pygame.display.flip()

    def run_stage_first_click(self):
        running = True
        while running and not self.should_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(self.field.field.closed, self.field.field.marked_bombs)
                    # print(f"Нажатие мыши в {event.pos}")
                    x, y = event.pos
                    if self.field.on_field(y, x):
                        if event.button == 1: # Левая кнопка
                            running = False
                            self.field.build_pygame(y, x)
                        elif event.button == 3: # Правая кнопка
                            pass
                        self.field.show_pygame()
            pygame.display.flip()

    def run_stage_next_clicks(self):
        last_click_time = 0
        while not self.should_quit and not self.field.is_finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(self.field.field.closed, self.field.field.marked_bombs)
                    # print(f"Нажатие мыши в {event.pos}")
                    x, y = event.pos
                    if event.button == 1: # Левая кнопка
                        is_double_click = pygame.time.get_ticks() - last_click_time < DOUBLE_CLICK_INTERVAL
                        last_click_time = pygame.time.get_ticks()

                        if (self.field.on_field(y, x)):
                            f = self.field.open_pygame(y, x, is_double_click)
                            if f == 9:
                                self.field.show_pygame_cells(y, x)
                            elif f == 1:
                                self.field.show_pygame_cell(y, x)
                            else:
                                self.field.show_pygame()

                    elif event.button == 3: # Правая кнопка
                        if (self.field.on_field(y, x)):
                            self.field.mark_pygame(y, x)
                            self.field.show_pygame_cell(y, x)

            pygame.display.flip()

    def run_stage_game_over(self):
        if self.field.field.lose:
            draw_text(self.screen, self.HEIGHT // 2, self.WIDTH // 2, self.HEIGHT // 3, RED, "LOSE", alpha=150)
            print("GG")
        else:
            draw_text(self.screen, self.HEIGHT // 2, self.WIDTH // 2, self.HEIGHT // 3, GOLDEN, "WIN", alpha=150)
            print("Win")
        pygame.display.flip()

        should_continue = False
        while not self.should_quit and not should_continue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    should_continue = True
