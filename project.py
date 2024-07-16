#ss
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
    def __init__(self, screen, color, x, y, radius, speed_x, speed_y):
        self.screen = screen
        self.color = color
        self.dist = 0
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.y = self.y + self.speed_y
        self.x = self.x + self.speed_x
        self.dist += 1

        if self.x <= 470 and self.y == 200:
            self.speed_x = 2
        elif 475 <= self.x <= 500 and self.y <= 470:
            self.speed_x = 0
            self.speed_y = 2
        elif self.x <= 700 and self.y >= 475:
            self.speed_x = 2
            self.speed_y = 0
        elif self.y >= 475 and self.x <= 1000:
            self.speed_x = 0
            self.speed_y = -2
        elif self.y <= 200 and self.x < 1000:
            self.speed_x = 2
            self.speed_y = 0
        elif self.x >= 1000 and self.y >= 200:
            self.speed_x = 0
            self.speed_y = -2

    def draw(self):
        pygame.draw.circle(self.screen, (225,75, 75), (self.x, self.y),
                 25)

class beamTurret:
    def __init__(self,screen,x,y,angle):
        self.screen =screen
        self.x =x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load('TowerDef_BeamTurret - Copy - Copy.png')
        self.baseImage = pygame.image.load('TowerDef_BeamTurret - Copy - Copy.png')
        self.validTarget = []
        self.targetnumber =0
        self.targetx=0
        self.targety=0
        self.newAngle = self.angle

    def draw(self):
        pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        self.screen.blit(self.image,(self.x-(self.image.get_width()/2), self.y-(self.image.get_height()/2)))
    def turn(self, angle):
        if angle < 10:
            self.newAngle = math.degrees(angle)
        self.image = pygame.transform.rotate(self.baseImage, self.newAngle)

    def shoot(self):
        print(self.angle)
        pygame.draw.line (self.screen,(255,100,100), (self.x, self.y),
                          (
                              (self.x + (math.cos(self.angle)*600)),
                              (self.y + (math.sin(self.angle)*600))
                          ),
                          20)
    def targetEnemy(self, active):   #TARGET FIRST ENEMY
        self.targetnumber = 0
        for enemy in active:
            if distance((self.x,self.y),(enemy.x,enemy.y)) <=300:
                self.validTarget.append(enemy)
        if len(self.validTarget)==0:
            return False
        else:
            while len(self.validTarget)>1:
                for enemy in self.validTarget:
                    if enemy.dist < self.targetnumber:
                        self.validTarget.remove(enemy)
                self.targetnumber+=1
            if len(self.validTarget)<=0:
                for enemy in active:
                    if distance((self.x, self.y), (enemy.x, enemy.y)) <= 300 and enemy.dist <= self.targetnumber:
                        self.validTarget.append(enemy)
                r = random.randint(0, (len(self.validTarget)-1))
                tar = self.validTarget[r]
                self.targetx = tar.x
                self.targety = tar.y
                self.angle = math.atan(tar.y / tar.x)
                self.turn(self.angle)
                return True
            else:
                tar = self.validTarget[0]
                self.targetx = tar.x
                self.targety = tar.y
                print(tar.x, tar.y)
                if tar.y >= self.y:
                    self.angle = math.acos((tar.x-self.x)/(distance((self.x,self.y),(tar.x,tar.y))))
                else:
                    self.angle = -1*math.acos((tar.x - self.x) / (distance((self.x, self.y), (tar.x, tar.y))))

                self.turn((self.angle*-1))

            return True
    def hitEnemy(self,enemy):
        hitbox = pygame.draw.line (self.screen,(255,100,100), (self.x, self.y),
                          (
                              (self.x + (math.cos(self.angle)*600)),
                              (self.y + (math.sin(self.angle)*600))
                          ),
                          20)

        if hitbox.collidepoint(enemy.x, enemy.y):
            print("HIT")
        return hitbox.collidepoint(enemy.x, enemy.y)


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
                Enemy = enemy(self.screen, (255, 255, 0), 5, 200, 50, 5, 0)
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
        pygame.draw.line(self.screen, (90, 140, 60), (0, 200),(500, 200),50)
        pygame.draw.line(self.screen, (90, 140, 60), (475, 180), (475, 500), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (475, 475), (725, 475), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (700, 475), (700, 176), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (700, 200), (1025, 200), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (1000, 200), (1000, 0), 50)


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

    UI = ui(screen)
    ion = 0
    test = beamTurret(screen, 500, 300,0.0)
    spawns = waveSpawn(screen, gamestate)
    activeEnemies = spawns.getList()

    #my_enemy = enemy(screen, (255, 255, 0), 5, 200, 50, 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)



        # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((75, 155, 75))

        PTH.draw()


        waves +=1
        spawns.spawns(1)
        activeEnemies = spawns.getList()
        gamestate = False
        spawns.updateState(gamestate)
        for enemy1 in activeEnemies:
            enemy1.move()
            enemy1.draw()
        key = pygame.key.get_pressed()
        #if key[pygame.K_SPACE]:

        if test.targetEnemy(activeEnemies):
            test.shoot()
            for enemy1 in activeEnemies:
                test.hitEnemy(enemy1)

        #if key[pygame.K_RIGHT]:
        #    test.turn(ion)
        #    ion += 10
        #if key[pygame.K_LEFT]:
        #    test.turn(ion)
        #    ion -= 10

        UI.draw()

        #    #TODO: MAKE UNIQUE WAVES

        test.draw()


        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()
