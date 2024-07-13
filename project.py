import pygame
import sys
import random
import time

#:) sdf hi

def main():
    # turn on pygame
    pygame.init()

    # create a screen
    pygame.display.set_caption("Tower Defense")
    # TODO: Change the size of the screen as you see fit!
    screen = pygame.display.set_mode((640, 480))

    # let's set the framerate
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)
            # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((255, 255, 255))

        # TODO: Add your project code

        # TODO: Add the map, and UI

        # TODO: LEARN TO TURN

        # TODO: Add enemies, towers, projectiles

        # TODO: Add lives, money, waves

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()
