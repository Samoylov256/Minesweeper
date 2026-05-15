from random import shuffle
import pygame



pygame.init()

class Field:
    def __init__(self, screen, height=10, width=10, percent=10):
        self.screen = screen
        self.closed = width * height
        self.marked_bombs = 0
        self.lose = False
        self.width = width
        self.height = height
        self.field = []
        self.graph = {}
        self.percent = percent
        self.vectors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        
        HEIGHT, WIDTH = screen.get_height(), screen.get_width()
        
        
        # drowing
        self.indent_h = 20
        self.indent_w = 20
        self.cell_h = min((WIDTH - 2 * self.indent_w) // width,
                          (HEIGHT - 2 * self.indent_h) // height)     # сделать нецелые
        
        field_line = [[0, 0] for i in range(height * width)]
        for i in range(height):
            self.field.append(field_line[width * i:width * i + width])


    def build(self, y, x):
        bombs = self.width * self.height * self.percent // 100
        height = self.height
        width = self.width
        
        # field[i][j][0]
            # bomb = -1
            # far from bomb = 0
            # near bomb > 0
        # field[i][j][1]
            # closed = 0
            # opened = 1
            # flag = 2
            # cross(wrong flag) = 3
        
        
        
        cutted_field_line = []
        
        pointer = 0
        hole = []
        # print(x, y)
        while (pointer < self.width * self.height):
            xx = pointer % self.width
            yy = pointer // self.width
            # print(xx, yy)
            if (not (x - 1 <= xx <= x + 1 and y - 1 <= yy <= y + 1)):
                if (bombs > 0):
                    cutted_field_line.append([-1, 0])
                    bombs -= 1
                else:
                    cutted_field_line.append([0, 0])
            else:
                hole.append(pointer)
            pointer += 1
        
        
        # print(hole)
        shuffle(cutted_field_line)
        
        
        field_line = []
        pointer = 0
        count_holes = 0
        while (pointer < self.width * self.height):
            if (pointer in hole):
                field_line.append([0, 0])
                count_holes += 1
            else:
                field_line.append(cutted_field_line[pointer - count_holes])
                # print(pointer, count_holes, pointer - count_holes)
            pointer += 1
        
        
        self.field = []
        for i in range(height):
            self.field.append(field_line[width * i:width * i + width])
        
       
        
        vectors = self.vectors
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j][0] == 0:
                    self.graph[(i, j)] = []
                    for t in vectors:
                        ii, jj = i + t[0], j + t[1]
                        if ii >= 0 and jj >= 0 and ii < self.height and jj < self.width:
                            if self.field[ii][jj][0] == -1:
                                self.field[i][j][0] += 1
                    if self.field[i][j][0] == 0:
                        self.graph[(i, j)] = []
                        for t in vectors:
                            ii, jj = i + t[0], j + t[1]
                            if ii >= 0 and jj >= 0 and ii < self.height and jj < self.width:
                                self.graph[(i, j)].append((ii, jj))
        self.open(y, x)
    
    
    def build_pygame(self, y, x):
        self.build((y - self.indent_h) // self.cell_h,
                   (x - self.indent_w) // self.cell_h)
    
    
    
    
    
    def is_finished(self):
        return self.lose or (self.closed - self.marked_bombs == 0)
    
    
    
    
    
    def show(self):
        for line in self.field:
            for j in line:
                if (j[0] == -1):
                    print(' * ', end='')
                elif (j[0] == 0):
                    print(' . ', end='')
                else:
                    print(f' {j[0]} ', end='')
            print('\n\n')


    def show_opened(self):
        for line in self.field:
            for j in line:
                if (j[1] == 0):    # closed
                    print(' ` ', end='')
                elif (j[1] == 1):  # opened
                    if (j[0] == 0):
                        print(' # ', end='')         # far from bomb
                    elif (j[0] == -1):
                        print(' * ', end='')        # bomb
                    else:
                        print(f' {j[0]} ', end='')   # near bomb
                elif (j[1] == 2):
                    print(' > ', end='')
                elif (j[1] == 3):
                    print(' ~ ', end='')
            print('\n\n')




    def open(self, h, w, double_click=False):
        # print(f'double_click={double_click}')
        if self.field[h][w][1] == 0:   # closed
            if self.field[h][w][0] == -1:   # bomb
                for i in range(self.height):
                    for j in range(self.width):
                        if self.field[i][j][0] == -1 and self.field[i][j][1] == 0:   # closed bomb
                            self.field[i][j][1] = 1   # open
                        if self.field[i][j][0] != -1 and self.field[i][j][1] == 2:   # marked unbomb
                            self.field[i][j][1] = 3   # wrong
                self.lose = True
            elif self.field[h][w][0] > 0:   # near bomb
                self.field[h][w][1] = 1
                self.closed -= 1
                return True
            else:                           # far from bomb
                current = [(h, w)]
                self.field[h][w][1] = 1
                self.closed -= 1
                while current:
                    new_current = []
                    for old in current:
                        for new in self.graph[old]:
                            if self.field[new[0]][new[1]][1] == 0:
                                if new in self.graph:
                                    new_current.append(new)
                                self.field[new[0]][new[1]][1] = 1
                                self.closed -= 1
                    current = new_current
            return False
        
        elif self.field[h][w][1] == 1 and self.field[h][w][0] > 0:   # opened near bomb
            if double_click:
                # print('почти')
                vectors = self.vectors
                c = 0
                for t in vectors:
                    hh, ww = h + t[0], w + t[1]
                    if hh >= 0 and ww >= 0 and hh < self.height and ww < self.width:
                        c += (self.field[hh][ww][1] == 2)
                if c == self.field[h][w][0]:
                    # print('good')
                    f = True
                    for t in vectors:
                        hh, ww = h + t[0], w + t[1]
                        if hh >= 0 and ww >= 0 and hh < self.height and ww < self.width:
                            if (self.field[hh][ww][1] == 0):
                                # print(f'good {hh} {ww}')
                                f = f and self.open(hh, ww)
                    return f * 9
        return True
    
    # pygame vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    

    def on_field(self, y, x):
        return (self.indent_h <= y < self.indent_h + self.cell_h * self.height and
        self.indent_w <= x < self.indent_w + self.cell_h * self.width)

    


    def open_pygame(self, y, x, double_click=False):
        return self.open((y - self.indent_h) // self.cell_h,
                         (x - self.indent_w) // self.cell_h,
                         double_click)
    
    
    

    def mark(self, h, w):           #  mark + unmark
        if self.field[h][w][1] == 0:    # closed
            self.field[h][w][1] = 2         # flag
            if self.field[h][w][0] == -1:   # bomb
                self.marked_bombs += 1
        elif self.field[h][w][1] == 2:  # marked
            self.field[h][w][1] = 0         # flag
            if self.field[h][w][0] == -1:   # bomb
                self.marked_bombs -= 1
    
    def mark_pygame(self, y, x):
        self.mark((y - self.indent_h) // self.cell_h, (x - self.indent_w) // self.cell_h)


    # pygame drawing vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    
    def draw_cell(self, h, w, colour, board=None):
        indent_h, indent_w = self.indent_h, self.indent_w
        cell_h = self.cell_h
        cell = self.field[h][w]
        if (board is not None):
            pygame.draw.rect(self.screen, colour,
                             (indent_w + w * cell_h, indent_h + h * cell_h, cell_h, cell_h), board)
        else:
            pygame.draw.rect(self.screen, colour,
                             (indent_w + w * cell_h, indent_h + h * cell_h, cell_h, cell_h))
    
    
    
    def draw_text(self, h, w, colour, text):
        indent_h, indent_w = self.indent_h, self.indent_w
        cell_h = self.cell_h
        cell = self.field[h][w]                        # del ?
        font = pygame.font.SysFont(None, cell_h)
        text_surface = font.render(text, True, colour)
        self.screen.blit(text_surface, (indent_w + w * cell_h + cell_h // 3, 
                                        indent_h + h * cell_h + cell_h // 5))
    
    
    
    def draw_polygon(self, h, w, colour, points=((0, 0), (50, 0), (0, 50))):
        indent_h, indent_w = self.indent_h, self.indent_w
        cell_h = self.cell_h
        cell = self.field[h][w]
        pygame.draw.polygon(self.screen, colour,
                tuple(map(
                    lambda t: (indent_w + w * cell_h + t[0] * cell_h // 100,
                               indent_h + h * cell_h + t[1] * cell_h // 100),
                            points)))
    
    def draw_image(self, h, w, colour, image):
        indent_h, indent_w = self.indent_h, self.indent_w
        cell_h = self.cell_h
        cell = self.field[h][w]
        scaled_image = pygame.transform.scale(image, (cell_h, cell_h))
        self.screen.blit(scaled_image, (indent_w + w * cell_h,
                                        indent_h + h * cell_h))
    
    
    
    def show_cell(self, h, w):
        indent_h, indent_w = self.indent_h, self.indent_w
        cell_h = self.cell_h
        cell = self.field[h][w]
        
        if (cell[1] == 0):    # closed
            self.draw_cell(h, w, GREEN)
        elif (cell[1] == 1):  # opened
            if (cell[0] == 0):
                self.draw_cell(h, w, BROWN)                 # far from bomb
            elif (cell[0] == -1):
                self.draw_cell(h, w, BROWN_GRAY)                # bomb
                self.draw_image(h, w, RED, explosion)
            else:
                self.draw_cell(h, w, BROWN)                 # near bomb
                self.draw_text(h, w, GREEN_EMERALD, str(cell[0]))
        elif (cell[1] == 2):                                # flag
            self.draw_cell(h, w, GREEN)
            self.draw_polygon(h, w, RED,
                              points=((25, 20), (30, 20), (80, 40), (30, 60),
                                      (30, 85), (35, 85), (35, 90), (20, 90),
                                      (20, 85), (25, 85)))
        elif (cell[1] == 3):  # cross
            self.draw_cell(h, w, GREEN)
            self.draw_polygon(h, w, RED,
                              points=((20, 25), (25, 20), (50, 45), (75, 20),
                                      (80, 25), (55, 50), (80, 75), (75, 80),
                                      (50, 55), (25, 80), (20, 75), (45, 50)))
        
            
        self.draw_cell(h, w, GREEN_DARK, 1)
        
    
    def show_pygame(self):
        self.screen.fill(GREEN_DARKEST)
        for i in range(self.height):
            for j in range(self.width):
                self.show_cell(i, j)
    
    def show_pygame_cell(self, y, x):
        i, j = (y - self.indent_h) // self.cell_h, (x - self.indent_w) // self.cell_h
        self.show_cell(i, j)
        
    def show_pygame_cells(self, y, x):
        i, j = (y - self.indent_h) // self.cell_h, (x - self.indent_w) // self.cell_h
        vectors = self.vectors
        for t in vectors:
            ii, jj = i + t[0], j + t[1]
            if ii >= 0 and jj >= 0 and ii < self.height and jj < self.width:
                self.show_cell(ii, jj)
    


explosion = pygame.image.load("explosion1.png")



BLACK = (0, 0, 0)
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

BLUE = (0, 0, 255)
