#s
import pygame
import sys
import random
import time
import math


        # TODO: Add your project code

        # TODO: Add the map, and UI

        # DONE: LEARN TO TURN

        # TODO: Add enemies, towers, projectiles

        # TODO: Add lives, money, waves
lives = 100
money = 500

class enemy:
    def __init__(self, screen, color, x, y, radius, speed_x, speed_y,):
        self.dist = 0
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y



    def move(self):
        self.dist +=1
        if self.x <= 470 and self.y == 200:
            self.speed_x = 5
        elif 470 <= self.x <= 500 and self.y <= 475:
            self.speed_x = 0
            self.speed_y = 5
            print(self.y)
        elif self.x <= 695 and self.y >= 470:
            self.speed_x = 5
            self.speed_y = 0
            print(self.y)
        elif self.y >= 200:
            self.speed_x = 0
            self.speed_y = -5
            print(self.y)
            print(self.x)




    def draw(self):
        pygame.draw.circle(self.screen, (225, 100, 100), (self.x, self.y),
                 25)
class beamTurret:
    def __init__(self,screen,x,y,angle,fireState):
        self.screen =screen
        self.x =x
        self.y = y
        self.angle = angle
        self.clock = pygame.time.Clock()
        self.fireState = fireState#True/False
        self.image = pygame.image.load('TowerDef_BeamTurret.png')
        self.baseImage = pygame.image.load('TowerDef_BeamTurret.png')
        self.validTarget = []
        self.targetnumber =0

    def draw(self):
        pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),10)
        self.screen.blit(self.image,(self.x-(self.image.get_width()/2), self.y-(self.image.get_height()/2)))
    def turn(self, angle):
        self.image = pygame.transform.rotate(self.baseImage,angle)
        self.angle = angle
    def shoot(self):
        pygame.draw.line(self.screen,(255,100,100), ((((self.y + (math.sin(math.radians(self.angle)))*-10)),
                         (self.x+(math.cos(math.radians(self.angle)))*-10))),
                         (((self.y + (math.sin(math.radians(self.angle)))*-600)),
                         (self.x+(math.cos(math.radians(self.angle)))*-600)),20)
    def targetEnemy(self, active):   #TARGET FIRST ENEMY
        self.targetnumber = 0
        for enemy in active:
            if distance((self.x,self.y),(enemy.x,enemy.y)) <=300:
                self.validTarget.append(enemy)
        while len(self.validTarget)>1:
            for enemy in self.validTarget:
                if enemy.dist < self.targetnumber:
                    self.validTarget.remove(enemy)
            self.targetnumber+=1
        if len(self.validTarget)<0:
            for enemy in active:
                if distance((self.x, self.y), (enemy.x, enemy.y)) <= 300 and enemy.dist <= self.targetnumber:
                    self.validTarget.append(enemy)
            r = random.randint(0, (len(self.validTarget)-1))
            tar = self.validTarget[r]
            self.angle = math.atan(tar.y * tar.x)
            return True
        else:
            tar = self.validTarget[0]
            self.angle = math.atan(tar.y * tar.x)
            return True
    def hitEnemy(self):
        hitbox = pygame.draw.line(self.screen,(255,100,100), ((((self.y + (math.sin(math.radians(self.angle)))*-10)),
                         (self.x+(math.cos(math.radians(self.angle)))*-10))),
                         (((self.y + (math.sin(math.radians(self.angle)))*-600)),
                         (self.x+(math.cos(math.radians(self.angle)))*-600)),20)

def distance(point1, point2):
    point1_x = point1[0]
    point2_x = point2[0]
    point1_y = point1[1]
    point2_y = point2[1]
    return math.sqrt((point2_x-point1_x)**2+(point2_y-point1_y)**2)
class waveSpawn:
    def __init__(self,screen,state):
        self.screen = screen
        self.wavespawn = []
        self.state = state
    def spawns(self,enemyTotal):
        if self.state:
            for _ in range(enemyTotal):
                Enemy = enemy(self.screen, (255, 255, 0), 5, 200, 50, 0, 0)
                self.wavespawn.append(Enemy)
    def getList(self):
        return self.wavespawn
    def updateState(self,state):
        self.state = state


class ui:
    def __init__(self,screen):
        self.screen = screen
        self.buy1x = 100
        self.buy2x = 400
        self.buy3x = 700
        self.buyy = 900
    def draw(self):
        pygame.draw.rect(self.screen, (0,0,0),(0,555,1080,75))

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
    gamestate = True
    waves = 0
    activeEnemies = []
    UI = ui(screen)
    ion = 0
    test = beamTurret(screen, 50, 50,0.0,False)
    spawns = waveSpawn(screen, gamestate)
    #my_enemy = enemy(screen, (255, 255, 0), 5, 200, 50, 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)
        waves +=1
        spawns.spawns(4)
        activeEnemies = spawns.getList()
        gamestate = False
        for enemy in activeEnemies:
            enemy.move()
            enemy.draw()

        # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((75, 155, 75))

        PTH.draw()



        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            test.targetEnemy(activeEnemies)
            test.shoot()
        if key[pygame.K_RIGHT]:
            test.turn(ion)
            ion += 10
        if key[pygame.K_LEFT]:
            test.turn(ion)
            ion -= 10

        UI.draw()

        #    #TODO: MAKE UNIQUE WAVES

        test.draw()


        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()
