import pygame
from game_scene import GameScene
from menu_scene import MenuScene
from game_settings import GameSettings


pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

settings = GameSettings()

while True:
    menu_scene = MenuScene(screen, settings)
    menu_scene.run()
    if menu_scene.should_quit:
        break
    settings = menu_scene.settings

    game_scene = GameScene(screen, settings.height, settings.width, settings.percent)
    game_scene.run()
    if game_scene.should_quit:
        break

pygame.quit()
