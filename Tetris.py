import pygame
import sys
import random

tab_offset = [[1, 1], [0, 0], [0, 0], [1, 1]]

# For J,L,S,T and Z
kick_offset = [
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],  # rotation index = 0
    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],  # rotation index = 1
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],  # rotation index = 2
    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]  # rotation index = 3
]

kick_offset_I = [
    [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)],  # rotation index = 0
    [(-1, 0), (0, 0), (0, 0), (0, 1), (0, -2)],  # rotation index = 1
    [(-1, 1), (1, 1), (-2, 1), (1, 0), (-2, 0)],  # rotation index = 2
    [(0, 1), (0, 1), (0, 1), (0, -1), (0, 2)]  # rotation index = 3
]

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 440

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE
LOWER_BOUND = GRID_HEIGHT - 2

# TODO : Implement rotation verification system
# TODO : Create a class for the game?
# TODO : Bloc falling if nothing under


ColorRef = {
    1: (43, 240, 233),  # cyan
    2: (242, 182, 78),  # orange
    3: (32, 64, 227),  # blue
    4: (233, 240, 43),  # yellow
    5: (43, 240, 82),  # green
    6: (191, 43, 240),  # purple
    7: (240, 43, 43)  # red
}


ColorRefDark = {
    1: (26, 145, 132),  # cyan
    2: (189, 139, 62),  # orange
    3: (25, 47, 163),  # blue
    4: (201, 207, 52),  # yellow
    5: (59, 184, 83),  # green
    6: (136, 45, 166),  # purple
    7: (166, 38, 38) # red
}

ColorRefLight = {
    1: (138, 255, 251),  # cyan
    2: (252, 213, 129),  # orange
    3: (98, 120, 224),  # blue
    4: (250, 255, 107),  # yellow
    5: (89, 255, 122),  # green
    6: (232, 97, 209),  # purple
    7: (255, 97, 97)  # red
}



TypeList = ["I", "J", "L", "O", "S", "T", "Z"]


def print_matrix(matrix):
    for row in matrix:
        print(row)


class Block(object):

    def __init__(self):
        self.type = random.choice(["I", "J", "L", "O", "S", "T", "Z"])
        self.blocks = []
        self.abs_pos = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.rotation_index = 0
        self.center_pos = [5, 0]
        self.color = (76, 75, 44)
        self.darkcolor = (0, 0, 0)
        self.ligthcolor = (0, 0, 0)
        self.active = True
        self.matrix_generated = False
        self.value_can_go_down = True
        self.value_can_go_left = True
        self.value_can_go_right = True
        self.generate_matrix()
        self.init_abs()
        # should be in a class called Game
        self.speed = 5

    def generate_matrix(self):

        if self.type == "I":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [2, 0]]
            self.color = ColorRef[1]  # cyan
            self.darkcolor = ColorRefDark[1]
            self.ligthcolor = ColorRefLight[1]

        elif self.type == "J":
            self.blocks = [[-1, 1], [-1, 0], [0, 0], [1, 0]]
            self.color = ColorRef[2]  # orange
            self.darkcolor = ColorRefDark[2]
            self.ligthcolor = ColorRefLight[2]

        elif self.type == "L":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [1, 1]]
            self.color = ColorRef[3]
            self.darkcolor = ColorRefDark[3]     # blue
            self.ligthcolor = ColorRefLight[3]

        elif self.type == "O":
            self.blocks = [[0, 0], [1, 1], [0, 1], [1, 0]]
            self.color =  ColorRef[4] # yellow
            self.darkcolor = ColorRefDark[4]
            self.ligthcolor = ColorRefLight[4]

        elif self.type == "S":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [1, 1]]
            self.color = ColorRef[5]  # green
            self.darkcolor = ColorRefDark[5]
            self.ligthcolor = ColorRefLight[5]

        elif self.type == "T":
            self.blocks = [[-1, 0], [0, 0], [0, 1], [1, 0]]
            self.color = ColorRef[6] # purple
            self.darkcolor = ColorRefDark[6]
            self.ligthcolor = ColorRefLight[6]

        elif self.type == "Z":
            self.blocks = [[-1, 1], [0, 1], [0, 0], [1, 0]]
            self.color = ColorRef[7]  # red
            self.darkcolor =  ColorRefDark[7]
            self.ligthcolor =  ColorRefLight[7]


    def cw_rotation(self):

        if self.type != "O":
            for block in self.blocks:
                new_x = 1 * block[1]
                new_y = -1 * block[0]
                block[0] = new_x
                block[1] = new_y
            self.rotation_index += 1
            self.rotation_index = (self.rotation_index % 4)

        if self.type == "I":
            x_offset = tab_offset[self.rotation_index - 1][0] - tab_offset[self.rotation_index][0]
            y_offset = tab_offset[self.rotation_index - 1][1] - tab_offset[self.rotation_index][1]
            self.center_pos[0] = self.center_pos[0] + x_offset
            self.center_pos[1] = self.center_pos[1] + y_offset

            self.init_abs()
            self.calculate_abs()

    def ccw_rotation(self):

        if self.type != "O":
            for block in self.blocks:
                new_x = -1 * block[1]
                new_y = 1 * block[0]
                block[0] = new_x
                block[1] = new_y
            self.rotation_index -= 1
            self.rotation_index = (self.rotation_index % 4)

        if self.type == "I":
            y_offset = tab_offset[(self.rotation_index + 1) % 4][0] - tab_offset[self.rotation_index][0]
            x_offset = tab_offset[(self.rotation_index + 1) % 4][1] - tab_offset[self.rotation_index][1]
            self.center_pos[0] = self.center_pos[0] + x_offset
            self.center_pos[1] = self.center_pos[1] + y_offset

            self.init_abs()
            self.calculate_abs()

    def calculate_abs(self):
        for i in range(len(self.abs_pos)):
            self.abs_pos[i][0] = self.blocks[i][0] + self.center_pos[0]
            self.abs_pos[i][1] = self.blocks[i][1] + self.center_pos[1]

    def init_abs(self):
        for i in range(len(self.abs_pos)):
            self.abs_pos[i][0] = self.blocks[i][0] + self.abs_pos[i][0] + self.center_pos[0]
            self.abs_pos[i][1] = self.blocks[i][1] + self.abs_pos[i][1] + self.center_pos[1]

    def handle_keys(self, matrix):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.can_go_left(matrix):
                    self.left()
                elif event.key == pygame.K_RIGHT and self.can_go_right(matrix):
                    self.right()
                elif event.key == pygame.K_UP:
                    self.ccw_rotation()
                elif event.key == pygame.K_DOWN:
                    self.cw_rotation()

                elif event.key == pygame.K_SPACE:
                    self.speed = 100

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.speed = 5

    def draw(self, surface):

        for block in self.abs_pos:
            r = pygame.Rect((block[0] * GRID_SIZE, block[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r, border_radius=0)
            pygame.draw.polygon(surface, self.darkcolor, ((block[0] * GRID_SIZE+20, block[1] * GRID_SIZE+20),
                                                       ((block[0] * GRID_SIZE), (block[1] * GRID_SIZE)+20),
                                                       ((block[0] * GRID_SIZE) + 5, block[1] * GRID_SIZE + 15),
                                                       ((block[0] * GRID_SIZE)+15, (block[1] * GRID_SIZE)+15),),
                                                        width=0)
            pygame.draw.polygon(surface, self.darkcolor, ((block[0] * GRID_SIZE+20, block[1] * GRID_SIZE),
                                                       ((block[0] * GRID_SIZE)+20, (block[1] * GRID_SIZE)+20),
                                                       ((block[0] * GRID_SIZE) + 15, block[1] * GRID_SIZE + 15),
                                                       ((block[0] * GRID_SIZE)+15, (block[1] * GRID_SIZE)+5),),
                                                        width=0)
            pygame.draw.polygon(surface, self.ligthcolor, ((block[0] * GRID_SIZE, block[1] * GRID_SIZE),
                                                       ((block[0] * GRID_SIZE), (block[1] * GRID_SIZE)+20),
                                                       ((block[0] * GRID_SIZE) + 5, block[1] * GRID_SIZE + 15),
                                                       ((block[0] * GRID_SIZE)+5, (block[1] * GRID_SIZE)+5),),
                                                        width=0)

            pygame.draw.polygon(surface, self.ligthcolor, ((block[0] * GRID_SIZE, block[1] * GRID_SIZE),
                                                       ((block[0] * GRID_SIZE)+20, (block[1] * GRID_SIZE)),
                                                       ((block[0] * GRID_SIZE) + 15, block[1] * GRID_SIZE + 5),
                                                       ((block[0] * GRID_SIZE)+5, (block[1] * GRID_SIZE)+5),),
                                                        width=0)





    def down(self):

        self.center_pos[1] = self.center_pos[1] + 1
        self.calculate_abs()

    def left(self):

        self.center_pos[0] = self.center_pos[0] - 1
        self.calculate_abs()
        self.value_can_go_right = True

    def right(self):
        self.center_pos[0] = self.center_pos[0] + 1
        self.calculate_abs()
        self.value_can_go_left = True

    def fill_matrix(self, matrix):

        for block in self.abs_pos:
            matrix.Grid[block[0]][block[1]] = (TypeList.index(self.type)) + 1
            matrix.NumberPerRow[block[1]] += 1

        self.matrix_generated = True

    def can_go_down(self, matrix):

        for block in self.abs_pos:
            if block[1] + 1 < 22:
                if matrix[block[0]][block[1] + 1] >= 1:
                    self.value_can_go_down = False

    def can_go_left(self, matrix):

        self.value_can_go_left = True
        for block in self.abs_pos:
            if matrix[block[0] - 1][block[1]] >= 1 or block[0] == 1:
                self.value_can_go_left = False

        return self.value_can_go_left

    def can_go_right(self, matrix):

        self.value_can_go_down = True
        for block in self.abs_pos:
            # Check if there is an element at the right in the matrix or the block if at the right border
            if matrix[block[0] + 1][block[1]] >= 1 or block[0] == 10:
                self.value_can_go_right = False

        return self.value_can_go_right

    def valid_pos(self, matrix):

        is_valid = True
        for block in self.abs_pos:
            if matrix[block[0]][block[1]] >= 1 or block[0] > 10 or block[0] < 1:
                is_valid = False
        return is_valid


class Matrix(object):

    def __init__(self):
        self.Width = 22
        self.Height = 12
        self.Grid = [[0 for x in range(self.Width)] for y in range(self.Height)]
        self.NumberPerRow = [0 for x in range(self.Width - 1)]

    def draw(self, surface):

        for i in range(len(self.Grid)):
            for y in range(len(self.Grid[i])):
                if self.Grid[i][y] >= 1:
                    rrr = pygame.Rect((i * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(surface, ColorRef[self.Grid[i][y]], rrr, border_radius=0)

                    pygame.draw.polygon(surface, ColorRefDark[self.Grid[i][y]], (
                                         (i * GRID_SIZE + 20, y * GRID_SIZE + 20),
                                         (i * GRID_SIZE, y * GRID_SIZE + 20),
                                         (i * GRID_SIZE + 5, y * GRID_SIZE + 15),
                                         (i * GRID_SIZE + 15, y * GRID_SIZE + 15)),width= 0)

                    pygame.draw.polygon(surface, ColorRefDark[self.Grid[i][y]], (
                        (i * GRID_SIZE + 20, y * GRID_SIZE),
                        (i * GRID_SIZE + 20, y * GRID_SIZE + 20),
                        (i * GRID_SIZE + 15, y * GRID_SIZE + 15),
                        (i * GRID_SIZE + 15, y * GRID_SIZE)), width=0)

                    pygame.draw.polygon(surface, ColorRefLight[self.Grid[i][y]], (
                        (i * GRID_SIZE , y * GRID_SIZE ),
                        (i * GRID_SIZE , y * GRID_SIZE + 20),
                        (i * GRID_SIZE + 5, y * GRID_SIZE + 15),
                        (i * GRID_SIZE + 5, y * GRID_SIZE + 5)),width= 0)


                    pygame.draw.polygon(surface, ColorRefLight[self.Grid[i][y]], (
                        (i * GRID_SIZE, y * GRID_SIZE),
                        (i * GRID_SIZE + 20, y * GRID_SIZE),
                        (i * GRID_SIZE + 15, y * GRID_SIZE + 5),
                        (i * GRID_SIZE + 5, y * GRID_SIZE+5)), width= 0)


    def draw_before_del(self, surface, line):

        for i in range(1, len(self.Grid)-1):

            rrr = pygame.Rect((i * GRID_SIZE, line * GRID_SIZE), (GRID_SIZE+1, GRID_SIZE+1))
            pygame.draw.rect(surface, (225, 225, 225), rrr)

    def remove_line(self, line):

        for col in self.Grid:
            del col[line]
            col.insert(0, 0)

    def check_line(self):

        value = -1
        for line in self.NumberPerRow:
            if line == 10:
                value = self.NumberPerRow.index(10)

        return value

    def print_matrix(self):

        for row in self.Grid:
            print(row)


def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):

            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (25, 25, 25), r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (20, 20, 20), rr)

            if (x == 0) or (y == 0) or x == (int(GRID_WIDTH) - 1) or y == (int(GRID_HEIGHT) - 1):
                rrr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (0, 0, 0), rrr)


def search(this_list, value):
    for i in range(len(this_list)):
        if this_list[i][1] == value:
            return True
    return False

def draw_square(surface):

    rrr = pygame.Rect((242, 190), (GRID_SIZE*5, GRID_SIZE*5))
    pygame.draw.rect(surface, (0, 0, 0), rrr, border_radius=0)






def main():

    new_block = Block()
    matrix = Matrix()
    next_block = Block()
    next_block.center_pos = [14, 10]  # for the preview

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH+120, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)
    my_font = pygame.font.SysFont("roboto", 16)

    i = 0
    score = 0
    end = False

    while True:


        clock.tick(new_block.speed)

        draw_grid(surface)
        draw_square(surface)
        matrix.draw(surface)



        if matrix.check_line() > 0:
            score += 1
            line = matrix.check_line()
            matrix.draw_before_del(surface, line)
            matrix.remove_line(line)
            del matrix.NumberPerRow[line]
            matrix.NumberPerRow.insert(0, 0)



        if not end:
            new_block.handle_keys(matrix.Grid)



        if end:
            rrr = pygame.Rect((60, 200), (GRID_SIZE * 12, GRID_SIZE * 3))
            pygame.draw.rect(surface, (50, 50, 50), rrr, border_radius=0)
            pygame.draw.rect(surface, (100, 100, 100), rrr, width = 5)

        new_block.draw(surface)
        next_block.calculate_abs()
        if not end:
            next_block.draw(surface)


        new_block.can_go_down(matrix.Grid)
        if (not (search(new_block.abs_pos, LOWER_BOUND))) and new_block.value_can_go_down:
            i = i + 1
            if i == 2:
                new_block.down()
                i = 0

        else:
            new_block.active = False

        if not new_block.active:
            if not new_block.matrix_generated:
                new_block.fill_matrix(matrix)
                if not end:

                    new_block.__init__()
                    new_block.type = next_block.type
                    new_block.color = next_block.color
                    new_block.generate_matrix()
                    new_block.calculate_abs()
                    new_block.can_go_down(matrix.Grid)

                    next_block.__init__()
                    next_block.center_pos = [14, 10]



                    if not new_block.value_can_go_down:
                        end = True

        screen.blit(surface, (0, 0))
        text_head = my_font.render("Score = {0}".format(score), True, (255, 255, 255))
        next = my_font.render("Next :", True, (255, 255, 255))
        screen.blit(next, (240, 160))

        if end:
            GameOver = my_font.render("Game Over, your score is = {0}".format(score), True, (255, 255, 255))
            screen.blit(GameOver, (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2))


        screen.blit(text_head, (240, 60))
        pygame.display.update()
        draw_grid(surface)
        matrix.draw(surface)
        pygame.init()


main()
