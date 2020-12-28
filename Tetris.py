import pygame
import sys
import random
import math


tab_offset = [[1, 1], [0, 0], [0, 0], [1, 1]]

SCREEN_WIDTH = 480
SCREEN_HEIGTH = 480


GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGTH = SCREEN_HEIGTH / GRID_SIZE
LOWER_BOUND = GRID_HEIGTH - 2

w, h = 23, 23
GameMatrix = [[0 for x in range(w)] for y in range(h)]


ColorRef = {
  1 : (43, 240, 233), #cyan
  2 : (242, 182, 78), #orange
  3 : (32, 64, 227),  #blue
  4:  (233, 240, 43), #yellow
  5:  (43, 240, 82),  #green
  6:  (191, 43, 240), #purple
  7:  (240, 43, 43) #red
}

TypeList = ["I", "J", "L", "O", "S", "T", "Z"]


def print_matrix(matrix):
    for row in matrix:
        print(row)

class Block(object):

    def __init__(self):
        self.type = random.choice(["I", "J", "L", "O", "S", "T", "Z"])
        self.type = "O"
        self.blocks = []
        self.abs_pos = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.rotation_index = 0
        self.center_pos = [11, 0]
        self.color = (76,75,44)
        self.active = True
        self.matrice_generated = False
        self.can_go_down = True
        self.generate_matrix()
        self.init_abs()

    def generate_matrix(self):

        if self.type == "I":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [2, 0]]
            self.color = (43, 240, 233) #cyan

        elif self.type == "J":
            self.blocks = [[-1, 1], [-1, 0], [0, 0], [1, 0]]
            self.color = (242, 182, 78) #orange

        elif self.type == "L":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [1, 1]]
            self.color = (32, 64, 227) #blue

        elif self.type == "O":
            self.blocks = [[0, 0], [1, 1], [0, 1], [1, 0]]
            self.color = (233, 240, 43) #yellow

        elif self.type == "S":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [1, 1]]
            self.color = (43, 240, 82) #green

        elif self.type == "T":
            self.blocks = [[-1, 0], [0, 0], [0, 1], [1, 0]]
            self.color = (191, 43, 240) #purple

        elif self.type == "Z":
            self.blocks = [[-1, 1], [0, 1], [0, 0], [1, 0]]
            self.color = (240, 43, 43) #red

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
            y_offset = tab_offset[(self.rotation_index+1)%4][0] - tab_offset[self.rotation_index][0]
            x_offset = tab_offset[(self.rotation_index+1)%4][1] - tab_offset[self.rotation_index][1]
            self.center_pos[0] = self.center_pos[0] + x_offset
            self.center_pos[1] = self.center_pos[1] + y_offset

            self.init_abs()
            self.calculate_abs()

    def calculate_abs(self):
       for i in range(len(self.abs_pos)):
            self.abs_pos[i][0] = self.blocks[i][0] + self.center_pos[0]
            self.abs_pos[i][1] = self.blocks[i][1] + self.center_pos[1]

    def init_abs(self):

        for block in self.abs_pos:
            block[0] = 0
            block[1] = 0



    def init_abs(self):
        for i in range(len(self.abs_pos)):
            self.abs_pos[i][0] = self.blocks[i][0] + self.abs_pos[i][0] + self.center_pos[0]
            self.abs_pos[i][1] = self.blocks[i][1] + self.abs_pos[i][1] + self.center_pos[1]

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.left()
                elif event.key == pygame.K_DOWN:
                    self.rigth()
                elif event.key == pygame.K_LEFT:
                    self.ccw_rotation()
                elif event.key == pygame.K_RIGHT:
                    self.cw_rotation()


    def draw(self, surface):

        for block in self.abs_pos:
            r = pygame.Rect((block[0] * GRID_SIZE, block[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)

    def down(self):

        self.center_pos[1] = self.center_pos[1] + 1
        self.calculate_abs()

    def left(self):
        self.center_pos[0] = self.center_pos[0] -1
        self.calculate_abs()

    def rigth(self):
        self.center_pos[0] = self.center_pos[0] +1
        self.calculate_abs()

    def fill_matrix(self, matrix):

        for block in self.abs_pos:
            print(block[0])
            print(block[1])
            matrix[block[0]][block[1]] = (TypeList.index(self.type)) + 1

        self.matrice_generated = True

    def Can_go_down(self, matrix):

        for block in self.abs_pos:
            if block[1]+1 < 22:
                 if matrix[block[0]][block[1]+1] >= 1:
                        self.can_go_down = False








def drawGrid(surface):
    for y in range(0,int(GRID_HEIGTH)):
        for x in range(0, int(GRID_WIDTH)):

            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE,y*GRID_SIZE), (GRID_SIZE,GRID_SIZE))
                pygame.draw.rect(surface,(25,25,25),r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (20, 20, 20), rr)

            if (x == 0) or (y == 0) or x == (int(GRID_HEIGTH)-1) or y == (int(GRID_HEIGTH)-1):
                rrr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (0, 0, 0), rrr)


def drawMatrix(surface, matrix):

    for i in range(len(matrix)):
        for y in range(len(matrix[i])):
            if GameMatrix[i][y] >= 1:
                rrr = pygame.Rect((i * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, ColorRef[matrix[i][y]], rrr)

def search(list, value):
    for i in range(len(list)):
        if list[i][1] == value:
            return True
    return False

#TODO supprimer la ligne
def DeleteLine(matrix):

    for line in matrix:
        i = 0
        for e in line:
            if e >= 1:
                i = i + 1
            if(i >= 21):
                print("DeleteLine")





def main():


    newblock = Block()

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_HEIGTH,SCREEN_HEIGTH), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)


    while True:

        clock.tick(5)

        drawGrid(surface)
        drawMatrix(surface, GameMatrix)

        newblock.handle_keys()
        newblock.draw(surface)

        newblock.Can_go_down(GameMatrix)
        print(newblock.can_go_down)
        if (not (search(newblock.abs_pos, LOWER_BOUND))) and newblock.can_go_down:
            newblock.down()

        else:
            newblock.active = False

        print(GameMatrix[10][21])
        if newblock.active == False:
            if newblock.matrice_generated == False:
                 newblock.fill_matrix(GameMatrix)
                 newblock.__init__()
                 newblock.type = "O"


        DeleteLine(GameMatrix)
        screen.blit(surface, (0, 0))
        pygame.display.update()







main()
