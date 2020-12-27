import pygame
import sys
import random
import math


tab_offset = [[1, 0], [0, 0], [-1, 0], [-2, 0]]

SCREEN_WIDTH = 480
SCREEN_HEIGTH = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGTH = SCREEN_HEIGTH / GRID_SIZE




class Block(object):

    def __init__(self):
        self.type = random.choice(["I", "J", "L", "O", "S", "T", "Z"])
        self.blocks = []
        self.abs_pos = []
        self.rotation_index = 0
        self.center_pos = [0, 0]

    def generate_matrix(self):

        if self.type == "I":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [2, 0]]

        elif self.type == "J":
            self.blocks = [[-1, 1], [-1, 0], [0, 0], [1, 0]]

        elif self.type == "L":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [1, 1]]

        elif self.type == "O":
            self.blocks = [[0, 0], [1, 1], [0, 1], [1, 0]]

        elif self.type == "S":
            self.blocks = [[-1, 0], [0, 0], [1, 0], [1, 1]]

        elif self.type == "T":
            self.blocks = [[-1, 0], [0, 0], [0, 1], [1, 0]]

        elif self.type == "Z":
            self.blocks = [[-1, 1], [0, 1], [0, 0], [1, 0]]

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

            for block in self.blocks:
                block[0] = block[0] + x_offset
                block[1] = block[1] + y_offset



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
            y_offset = tab_offset[self.rotation_index+1][0] - tab_offset[self.rotation_index][0]
            x_offset = tab_offset[self.rotation_index+1][1] - tab_offset[self.rotation_index][1]

            for block in self.blocks:
                block[0] = block[0] + x_offset
                block[1] = block[1] + y_offset

    def calculate_abs(self):

        self.abs_pos.clear()

        for i in range(len(self.blocks)):
            abs_x = self.blocks[i][0] + self.center_pos[0]
            abs_y = self.blocks[i][1] + self.center_pos[1]
            self.abs_pos.append([abs_x, abs_y])

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_LEFT:
                    self.ccw_rotation()
                elif event.key == pygame.K_RIGHT:
                    self.cw_rotation()

    def draw(self, surface):

        for block in self.abs_pos:
            r = pygame.Rect((block[0] * GRID_SIZE, block[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (122, 45, 77), r)



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




def main():

    newblock = Block()
    newblock.type = "I"
    newblock.generate_matrix()
    newblock.center_pos = [5, 5]
    newblock.calculate_abs()


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_HEIGTH,SCREEN_HEIGTH),0,32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    while True:

        clock.tick(15)
        drawGrid(surface)

        newblock.handle_keys()

        newblock.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()

main()
