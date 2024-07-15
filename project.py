import pygame
import sys
import random
import time
import math


        # TODO: Add your project code

        # TODO: Add the map, and UI

        # TODO: LEARN TO TURN

        # TODO: Add enemies, towers, projectiles

        # TODO: Add lives, money, waves
#:) sdf
lives = 100
money = 500
waves = 0
gamestate = 0
class ui:
    def __init__(self,screen):
        self.screen = screen
        self.buy1x = 100
        self.buy2x = 400
        self.buy3x = 700
        self.buyy = 900
    def draw(self):

    def purchase(self,mousex,mousey,mouseDown):
        if mouseDown: #boolean
            if mousey >= self.buyy and mousey:
                if mousex >= self.buy1x-20 and mousey <= self.buy1x:
                    return 1


class path: # TODO: Make enemies move on the path
    def __init__(self, screen):
        self.screen = screen
    def draw(self):
        pygame.draw.line(self.screen, (0, 0, 255), (0, 200),(500, 200),50)
        pygame.draw.line(self.screen, (0, 0, 255), (475, 180), (475, 500), 50)
        pygame.draw.line(self.screen, (0, 0, 255), (475, 475), (700, 475), 50)
        pygame.draw.line(self.screen, (0, 0, 255), (700, 475), (700, 200), 50)

def main():
    # turn on pygame
    pygame.init()

    # create a screen
    pygame.display.set_caption("Tower Defense")
    # TODO: Change the size of the screen as you see fit!
    screen = pygame.display.set_mode((1080, 620))
    # let's set the framerate
    clock = pygame.time.Clock()
    PTH = path(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)

            # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((75, 155, 75))

        PTH.draw()

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()
