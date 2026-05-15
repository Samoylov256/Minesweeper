import pygame
import pygame_gui
from dataclasses import dataclass

from game_settings import GameSettings, read_game_settings


MENU_THEME_PATH = '../res/menu_theme.json'

IMAGE_BACKGROUND = pygame.image.load("../res/background.jpg")


class MenuScene:
    def __init__(self, screen, settings):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.manager = pygame_gui.UIManager(screen.get_size(), MENU_THEME_PATH)
        self.should_quit = False
        self.settings = settings

        center_x = self.width // 2
        form_left = center_x - 160
        input_left = center_x + 10
        row_top = 230
        row_gap = 70

        self.width_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(form_left, row_top, 140, 42),
            text="Ширина поля",
            manager=self.manager
        )
        self.width_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(input_left, row_top, 150, 42),
            manager=self.manager
        )
        self.width_input.set_allowed_characters("numbers")
        self.width_input.set_text(str(self.settings.width))

        self.height_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(form_left, row_top + row_gap, 140, 42),
            text="Высота поля",
            manager=self.manager
        )
        self.height_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(input_left, row_top + row_gap, 150, 42),
            manager=self.manager
        )
        self.height_input.set_allowed_characters("numbers")
        self.height_input.set_text(str(self.settings.height))

        self.percent_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(form_left, row_top + row_gap * 2, 140, 42),
            text="Мин, %",
            manager=self.manager
        )
        self.percent_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(input_left, row_top + row_gap * 2, 150, 42),
            manager=self.manager
        )
        self.percent_input.set_allowed_characters("numbers")
        self.percent_input.set_text(str(self.settings.percent))

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(center_x - 90, row_top + row_gap * 3 + 20, 180, 52),
            text="Играть",
            manager=self.manager
        )

        self.error_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(center_x - 340, self.height - 108, 680, 46),
            text="",
            manager=self.manager,
            object_id="#error_message"
        )

        self.focus_controls = [
            self.start_button,
            self.width_input,
            self.height_input,
            self.percent_input,
        ]
        self.set_focus(0)

        self.clock = pygame.time.Clock()
        
        self.image_background = pygame.transform.scale(IMAGE_BACKGROUND,
                                                       (self.width, self.height))

    def run(self):
        should_start_game = False

        while not self.should_quit and not should_start_game:
            time_delta = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        step = -1 if event.mod & pygame.KMOD_SHIFT else 1
                        self.move_focus(step)
                        continue
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.read_settings():
                            should_start_game = True
                        continue
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        if self.read_settings():
                            should_start_game = True

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.blit(self.image_background, (0, 0))
        # self.screen.fill('white')
        self.manager.draw_ui(self.screen)

    def set_focus(self, index):
        focused_control = self.focus_controls[index % len(self.focus_controls)]
        self.manager.set_focus_set(focused_control)

    def move_focus(self, step):
        self.set_focus(self.get_focus_index() + step)

    def get_focus_index(self):
        for index, control in enumerate(self.focus_controls):
            if control.is_focused:
                return index
        return 0

    def read_settings(self):
        settings, error_text = read_game_settings(
            self.width_input.get_text(),
            self.height_input.get_text(),
            self.percent_input.get_text(),
        )
        self.error_label.set_text(error_text)
        if settings is None:
            return False
        self.settings = settings
        return True
