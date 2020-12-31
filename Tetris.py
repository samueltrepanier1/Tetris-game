import pygame
import sys
import random
import math


tab_offset = [[1, 1], [0, 0], [0, 0], [1, 1]]

SCREEN_WIDTH = 240
SCREEN_HEIGTH = 440


GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGTH = SCREEN_HEIGTH / GRID_SIZE
LOWER_BOUND = GRID_HEIGTH - 2


w, h = 22, 12
GameMatrix = [[0 for x in range(w)] for y in range(h)]
NumberPerRow = [0 for x in range(w-1)]

#TODO : Fix bug with the border (can_go_left or can_go_rigth) stay false
#TODO : Implement rotation verification system
#TODO : Create a class for the matrix and the game?
#TODO : Stop condition (game over?)

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
        self.blocks = []
        self.abs_pos = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.rotation_index = 0
        self.center_pos = [5, 0]
        self.color = (76, 75, 44)
        self.active = True
        self.matrice_generated = False
        self.can_go_down = True
        self.can_go_left = True
        self.can_go_right = True
        self.generate_matrix()
        self.init_abs()
        #should be in a class called Game
        self.speed = 5

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

    def handle_keys(self, matrix):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.Can_go_left(matrix):
                    self.left()
                elif event.key == pygame.K_RIGHT and self.Can_go_right(GameMatrix):
                    self.rigth()
                elif event.key == pygame.K_UP:
                    self.ccw_rotation()
                elif event.key == pygame.K_DOWN:
                    self.cw_rotation()

                elif event.key == pygame.K_SPACE:
                    self.speed = 30

            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.speed = 5


    def draw(self, surface):

        for block in self.abs_pos:
            r = pygame.Rect((block[0] * GRID_SIZE, block[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r, border_radius=3,)
            pygame.draw.rect(surface, (255, 255, 255), r, border_radius=3, width=2)


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
                  matrix[block[0]][block[1]] = (TypeList.index(self.type)) + 1
                  NumberPerRow[block[1]] += 1

        self.matrice_generated = True


    def Can_go_down(self, matrix):

        for block in self.abs_pos:
            if block[1]+1 < 22:
                 if matrix[block[0]][block[1]+1] >= 1:
                        self.can_go_down = False

    def Can_go_left(self, matrix):

        self.can_go_left = True
        for block in self.abs_pos:
            if matrix[block[0]-1][block[1]] >= 1 or block[0] == 1:
                self.can_go_left = False

        return self.can_go_left

    def Can_go_right(self, matrix):

        self.can_go_down = True
        for block in self.abs_pos:
            #Check if there is an element at the rigth in the matrix or the block if at the rigth border
            if matrix[block[0]+1][block[1]] >= 1 or block[0] == 10:
                self.can_go_right = False

        return self.can_go_right





def drawGrid(surface):
    for y in range(0,int(GRID_HEIGTH)):
        for x in range(0, int(GRID_WIDTH)):

            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE,y*GRID_SIZE), (GRID_SIZE,GRID_SIZE))
                pygame.draw.rect(surface,(25,25,25),r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (20, 20, 20), rr)

            if (x == 0) or (y == 0) or x == (int(GRID_WIDTH)-1) or y == (int(GRID_HEIGTH)-1):
                rrr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (0, 0, 0), rrr)


def drawMatrix(surface, matrix):

    for i in range(len(matrix)):
        for y in range(len(matrix[i])):
            if GameMatrix[i][y] >= 1:
                rrr = pygame.Rect((i * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, ColorRef[matrix[i][y]], rrr, border_radius=3,)
                pygame.draw.rect(surface, (255,255,255), rrr, border_radius=3, width = 2)


def search(list, value):
    for i in range(len(list)):
        if list[i][1] == value:
            return True
    return False


def removeLineMatrix(Matrix, Line):

   for col in Matrix:
       del col[Line]
       col.insert(0,0)

def checkLine(LineArray):

    value = -1
    for line in LineArray:
        if line == 10:
          value = LineArray.index(10)

    return value








def main():


    newblock = Block()

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGTH), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)
    i = 0
    myfont = pygame.font.SysFont("monospace", 16)
    score = 0


    while True:

        clock.tick(newblock.speed)





        if (checkLine(NumberPerRow) > 0):
            score += 1
            Line = checkLine(NumberPerRow)
            removeLineMatrix(GameMatrix,Line)
            del NumberPerRow[Line]
            NumberPerRow.insert(0, 0)




        drawGrid(surface)
        drawMatrix(surface, GameMatrix)

        newblock.handle_keys(GameMatrix)
        newblock.draw(surface)

        newblock.Can_go_down(GameMatrix)
        if (not (search(newblock.abs_pos, LOWER_BOUND))) and newblock.can_go_down:
            i = i + 1
            if i == 2:
                 newblock.down()
                 i = 0

        else:
            newblock.active = False


        if newblock.active == False:
            if newblock.matrice_generated == False:
                 newblock.fill_matrix(GameMatrix)
                 newblock.__init__()

        screen.blit(surface, (0, 0))



        text_head = myfont.render("Score = {0}".format(score), 1, (255, 255, 255))
        screen.blit(text_head, (5, 0))

        pygame.display.update()



        drawGrid(surface)
        drawMatrix(surface, GameMatrix)



main()
