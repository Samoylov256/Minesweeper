from field_data import FieldData, CellState, CellBase
import pygame


pygame.init()


GREEN_DARKEST = (30, 90, 0)
GREEN = (50, 150, 0)
GREEN_DARK = (40, 120, 0)
GREEN_EMERALD = (0, 255, 0)

DIGIT_COLORS = {
    1: (0, 0, 255),       # синий
    2: (0, 255, 40),      # зелёный
    3: (255, 0, 0),       # красный
    4: (255, 255, 0),     # жёлтый
    5: (0, 255, 255),     # голубой
    6: (0, 255, 128),     # бирюзовый
    7: (20, 20, 20),      # почти чёрный
    8: (255, 255, 255),   # белый
}

IMAGES_GRASS_EMPTY = [pygame.image.load(f"../res/grass_empty_{i}.png") for i in range(1, 4)]
IMAGE_GRASS_FLAG = pygame.image.load("../res/grass_flag.png")
IMAGE_GRASS_CROSS = pygame.image.load("../res/grass_cross.png")
IMAGE_GROUND_EMPTY = pygame.image.load("../res/ground_empty.png")
IMAGE_GROUND_EXPLOSION = pygame.image.load("../res/ground_explosion.png")

IMAGE_WALL = pygame.image.load("../res/wall.png")




class FieldView:
    def __init__(self, screen, height=10, width=10, percent=10):
        self.field = FieldData(height, width, percent)
        self.screen = screen

        WIDTH, HEIGHT = screen.get_size()

        self.indent_h = 20
        self.indent_w = 20
        self.cell_h = min((WIDTH - 2 * self.indent_w) // width,
                          (HEIGHT - 2 * self.indent_h) // height)
        self.indent_h = (HEIGHT - self.cell_h * height) // 2
        self.indent_w = (WIDTH - self.cell_h * width) // 2

        self.cell_font = pygame.font.SysFont(None, self.cell_h)

        cell_size = (self.cell_h, self.cell_h)
        self.images_grass_empty = [pygame.transform.scale(image, cell_size) for image in IMAGES_GRASS_EMPTY]
        self.image_grass_flag = pygame.transform.scale(IMAGE_GRASS_FLAG, cell_size)
        self.image_grass_cross = pygame.transform.scale(IMAGE_GRASS_CROSS, cell_size)
        self.image_ground_empty = pygame.transform.scale(IMAGE_GROUND_EMPTY, cell_size)
        self.image_ground_explosion = pygame.transform.scale(IMAGE_GROUND_EXPLOSION, cell_size)
        self.image_wall = pygame.transform.scale(IMAGE_WALL, cell_size)


    def to_cell_pos(self, y, x):
        # Screen coordiantes to cell position
        cell_y = max(0, min(self.field.height - 1, (y - self.indent_h) // self.cell_h))
        cell_x = max(0, min(self.field.width - 1, (x - self.indent_w) // self.cell_h))
        # print(f'to_cell_pos({y}, {x}) -> {cell_y, cell_x}')
        return cell_y, cell_x

    def cell_left(self, x):
        # Cell left coordinate on screen
        return self.indent_w + x * self.cell_h

    def cell_top(self, y):
        # Cell top coordinate on screen
        return self.indent_h + y * self.cell_h

    def on_field(self, y, x):
        return (self.indent_h <= y < self.indent_h + self.cell_h * self.field.height and
            self.indent_w <= x < self.indent_w + self.cell_h * self.field.width)

    def is_finished(self):
        return self.field.is_finished()

    def build_pygame(self, y, x):
        self.field.build(*self.to_cell_pos(y, x))

    def open_pygame(self, y, x, double_click=False):
        return self.field.open(*self.to_cell_pos(y, x), double_click)

    def mark_pygame(self, y, x):
        self.field.mark(*self.to_cell_pos(y, x))

    def draw_cell(self, y, x, colour, width=0):
        cell_h = self.cell_h
        rect = (self.cell_left(x), self.cell_top(y), cell_h, cell_h)
        pygame.draw.rect(self.screen, colour, rect, width)

    def draw_text(self, y, x, colour, text):
        cell_h = self.cell_h
        text_surface = self.cell_font.render(text, True, colour)
        origin = (self.cell_left(x) + cell_h // 3, self.cell_top(y) + cell_h // 5)
        self.screen.blit(text_surface, origin)

    def draw_polygon(self, y, x, colour, points):
        dx = self.cell_left(x)
        dy = self.cell_top(y)
        scale = self.cell_h / 100
        scaled_points = [(dx + px * scale, dy + py * scale) for (px, py) in points]
        pygame.draw.polygon(self.screen, colour, scaled_points)

    def draw_cell_image(self, y, x, image):
        self.screen.blit(image, (self.cell_left(x), self.cell_top(y)))

    def show_cell(self, y, x):
        # print(f'show_cell({y}, {x})')
        cell = self.field.field[y][x]
        if cell.state == CellState.CLOSED:
            image = self.images_grass_empty[hash((y, x)) % len(self.images_grass_empty)]
            self.draw_cell_image(y, x, image)
        elif cell.state == CellState.OPENED:
            if cell.base == CellBase.BOMB:    # bomb
                self.draw_cell_image(y, x, self.image_ground_explosion)
            elif cell.base == CellBase.WALL:
                self.draw_cell_image(y, x, self.image_wall)
            else:
                self.draw_cell_image(y, x, self.image_ground_empty)
                if cell.base > 0:
                    self.draw_text(y, x, DIGIT_COLORS[cell.base], str(cell.base))
        elif cell.state == CellState.FLAG:
            self.draw_cell_image(y, x, self.image_grass_flag)
        elif cell.state == CellState.CROSS:
            self.draw_cell_image(y, x, self.image_grass_cross)
        # self.draw_cell(y, x, GREEN_DARK, 1)

    def show_pygame(self):
        self.screen.fill(GREEN_DARKEST)
        for y in range(self.field.height):
            for x in range(self.field.width):
                self.show_cell(y, x)

    def show_pygame_cell(self, y, x):
        self.show_cell(*self.to_cell_pos(y, x))

    def show_pygame_cells(self, y, x):
        cell_y, cell_x = self.to_cell_pos(y, x)
        for dy, dx in self.field.vectors:
            other_y, other_x = cell_y + dy, cell_x + dx
            if self.field.is_valid_pos(other_y, other_x):
                self.show_cell(other_y, other_x)
