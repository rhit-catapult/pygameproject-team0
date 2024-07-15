import pygame
import sys
import random
import time
import math

#CODE: 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
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
        self.buyy = 570
    def draw(self):
        pygame.draw.rect(self.screen, (50,50,50),(0,550,1080,100))

        pygame.draw.rect(self.screen, (150,150,150),(980,0,100,620))
        pygame.draw.circle(self.screen,(150,150,150),(self.buy1x,self.buyy),20)
    def purchase(self,mousex,mousey,mouseDown):
        if mouseDown: #boolean
            if mousey >= self.buyy-10 and mousey <= self.buyy+10:
                if mousex >= self.buy1x-10 and mousey <= self.buy1x+10:
                    return 1
                elif mousex >= self.buy2x-10 and mousey <= self.buy2x+10:
                    return 2
                elif mousex >= self.buy3x-10 and mousey <= self.buy3x+10:
                    return 3


class path: # TODO: Make enemies move on the path
    def __init__(self, screen):
        self.screen = screen
    def draw(self):
        pygame.draw.line(self.screen, (0, 0, 255), (0, 200),(500, 200),50)
        pygame.draw.line(self.screen, (0, 0, 255), (475, 180), (475, 500), 50)
        pygame.draw.line(self.screen, (0, 0, 255), (475, 475), (700, 475), 50)
        pygame.draw.line(self.screen, (0, 0, 255), (700, 500), (700, 150), 50)
        pygame.draw.line(self.screen, (0, 0, 255), (700, 175), (1080, 175), 50)

class beamTurret:
    def __init__(self,screen,x,y,angle):
        self.image = pygame.image.load('TowerDef_BeamTurret.png')
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = angle
    def draw(self):
        self.screen.blit(self.image,(self.x, self.y))
    def target(self):
        hitbox = pygame.draw.circle

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
    UI = ui(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)

            # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((75, 155, 75))

        PTH.draw()
        UI.draw()


        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()
