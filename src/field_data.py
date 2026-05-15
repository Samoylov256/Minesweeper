import random
from dataclasses import dataclass


class CellState:
    CLOSED = 0
    OPENED = 1
    FLAG = 2
    CROSS = 3 # wrong flag


class CellBase:
    BOMB = -1
    WALL = -2
    # far from bomb = 0, near bomb > 0

@dataclass
class Cell:
    base: int   # CellBase
    state: int   # CellState


class FieldData:
    def __init__(self, height=10, width=10, percent=10):
        self.closed = width * height
        self.marked_bombs = 0
        self.lose = False
        self.width = width
        self.height = height
        self.wall_height = 7
        self.wall_width = 10
        self.percent = percent
        self.vectors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.field = [[Cell(0, CellState.CLOSED) for _ in range(width)] for _ in range(height)]

    def is_valid_pos(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def build(self, start_y, start_x):
        # print(f'build({start_y}, {start_x})')
        height = self.height
        width = self.width
        bomb_count = width * height * self.percent // 100

        # Определение положений стен
        wall_positions = []
        for y in range(height):
            for x in range(width):
                if abs(start_x - x) <= 1 and abs(start_y - y) <= 1:
                    continue
                if (x + 1) % self.wall_width == 0 or (y + 1) % self.wall_height == 0:
                    wall_positions.append((y, x))
        wall_positions = set(random.sample(wall_positions,
                                           len(wall_positions) // 2))
        print(wall_positions)
        # Определение положений бомб
        bomb_positions = []
        for y in range(height):
            for x in range(width):
                if (y, x) in wall_positions:
                    continue
                if abs(start_x - x) <= 1 and abs(start_y - y) <= 1:
                    continue
                bomb_positions.append((y, x))
        bomb_count = min(bomb_count, len(bomb_positions))
        bomb_positions = set(random.sample(bomb_positions, bomb_count))

        # Создание поля
        self.field = []
        for y in range(height):
            field_line = []
            for x in range(width):
                if (y, x) in bomb_positions:
                    base_value = CellBase.BOMB
                elif (y, x) in wall_positions:
                    base_value = CellBase.WALL
                else:
                    base_value = 0
                field_line.append(Cell(base_value, CellState.CLOSED))
            self.field.append(field_line)

        # Расстановка чисел
        for y in range(height):
            for x in range(width):
                cell = self.field[y][x]
                if cell.base != 0:
                    continue
                for dy, dx in self.vectors:
                    yy, xx = y + dy, x + dx
                    if self.is_valid_pos(yy, xx) and self.field[yy][xx].base == CellBase.BOMB:
                        cell.base += 1

        self.open(start_y, start_x)
        # self.show()

    def is_finished(self):
        return self.lose or (self.closed - self.marked_bombs == 0)

#     def show(self):
#         for line in self.field:
#             for j in line:
#                 if (j.base == CellBase.BOMB):
#                     print(' * ', end='')
#                 elif (j.base == 0):
#                     print(' . ', end='')
#                 else:
#                     print(f' {j.base} ', end='')
#             print('\n\n')

#     def show_opened(self):
#         for line in self.field:
#             for j in line:
#                 if (j.state == CellState.CLOSED):
#                     print(' ` ', end='')
#                 elif (j.state == CellState.OPENED):
#                     if (j.base == 0):
#                         print(' # ', end='')
#                     elif (j.base == CellBase.BOMB):
#                         print(' * ', end='')
#                     else:
#                         print(f' {j.base} ', end='')
#                 elif (j.state == CellState.FLAG):
#                     print(' > ', end='')
#                 elif (j.state == CellState.CROSS):
#                     print(' ~ ', end='')
#             print('\n\n')

    def open(self, click_y, click_x, double_click=False):
        click_cell = self.field[click_y][click_x]
        if click_cell.state == CellState.CLOSED:
            print('CellState.CLOSED')
            if click_cell.base == CellBase.BOMB:   # bomb
                for y in range(self.height):
                    for x in range(self.width):
                        cell = self.field[y][x]
                        if cell.base == CellBase.BOMB:
                            if cell.state == CellState.CLOSED:
                                cell.state = CellState.OPENED
                        else:
                            if cell.state == CellState.FLAG:
                                cell.state = CellState.CROSS
                self.lose = True
            elif click_cell.base > 0:   # near bomb
                print('near bomb')
                click_cell.state = CellState.OPENED
                self.closed -= 1
                return True
            elif click_cell.base == 0:  # far from bomb
                print('far from bomb')
                click_cell.state = CellState.OPENED
                self.closed -= 1
                # Open area
                stack = [(click_y, click_x)]
                while stack:
                    y, x = stack.pop()
                    for dy, dx in self.vectors:
                        new_y, new_x = y + dy, x + dx
                        if not self.is_valid_pos(new_y, new_x):
                            continue
                        new_cell = self.field[new_y][new_x]
                        if new_cell.state != CellState.CLOSED:
                            continue
                        new_cell.state = CellState.OPENED
                        self.closed -= 1
                        if new_cell.base == 0:
                            stack.append((new_y, new_x))
            elif click_cell.base == CellBase.WALL:
                print('wall')
                click_cell.state = CellState.OPENED
                self.closed -= 1
                return True
            return False

        elif click_cell.state == CellState.OPENED and click_cell.base > 0:   # opened near bomb
            if double_click:
                print('почти')
                c = 0    # число флажков
                for dy, dx in self.vectors:
                    yy, xx = click_y + dy, click_x + dx
                    if self.is_valid_pos(yy, xx):
                        c += (self.field[yy][xx].state == CellState.FLAG)
                if c == click_cell.base:    # поставнено нужное число флажков
                    print('good')
                    f = True
                    for dy, dx in self.vectors:
                        yy, xx = click_y + dy, click_x + dx
                        if self.is_valid_pos(yy, xx):
                            if self.field[yy][xx].state == CellState.CLOSED:
                                print(f'good {yy} {xx}')
                                f = self.open(yy, xx) and f
                    return f * 9
        return True

    def mark(self, y, x):
        # mark/unmark
        cell = self.field[y][x]
        if cell.state == CellState.CLOSED:
            cell.state = CellState.FLAG
            if cell.base == CellBase.BOMB:
                self.marked_bombs += 1
        elif cell.state == CellState.FLAG:
            cell.state = CellState.CLOSED
            if cell.base == CellBase.BOMB:
                self.marked_bombs -= 1
