#ss
import pygame
import sys
import random
import time
import math


class enemy:
    def __init__(self, screen, color, x, y, radius, speed_x, speed_y,health,speed):
        self.dist = 0
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.health = health
        self.maxHealth = health
        self.speed = speed
        self.slowedSpeed = (speed*2)/3
        self.name = random.randint(0,500)
        self.slowed = False

    def updateSlowed(self,slowed):
        self.slowed=slowed
        if self.speed == 1:
            self.slowed = False

    def move(self):

        self.y = self.y + self.speed_y
        self.x = self.x + self.speed_x
        self.dist += self.speed

        if self.x <= 470 and self.y == 200:
            if self.slowed:
                self.speed_x = self.slowedSpeed
            else:
                self.speed_x = self.speed
        elif 475 <= self.x <= 500 and self.y <= 470:
            self.speed_x = 0
            if self.slowed:
                self.speed_y = self.slowedSpeed
            else:
                self.speed_y = self.speed
        elif self.x <= 700 and self.y >= 475:
            if self.slowed:
                self.speed_x = self.slowedSpeed
            else:
                self.speed_x = self.speed
            self.speed_y = 0
        elif self.y >= 475 and self.x <= 1000:
            self.speed_x = 0
            if self.slowed:
                self.speed_y = -self.slowedSpeed
            else:
                self.speed_y = -self.speed
        elif self.y <= 200 and self.x < 1000:
            if self.slowed:
                self.speed_x = self.slowedSpeed
            else:
                self.speed_x = self.speed
            self.speed_y = 0
        elif self.x >= 1000 and self.y >= 180:
            self.speed_x = 0
            if self.slowed:
                self.speed_y = -self.slowedSpeed
            else:
                self.speed_y = -self.speed
    def offscreen(self):
        if self.y < 0:
            return True
    def offscreen2(self):
        if self.y < 0:
            if self.health < 1:
                self.health = 1
            return self.health
    def damage(self,dam):
        self.health -=dam
        return dam
    def deathCheck(self):
        if self.health <=0:
            self.dist = -1
            return True
    def deathCheck2(self):
        if self.health <=0:

            return self.health

    def draw(self):
        pygame.draw.circle(self.screen, (self.color), (self.x, self.y),
                 25)
        pygame.draw.line(self.screen,(255,0,0),((self.x-10),(self.y+10)),((self.x+10),(self.y+10)),7)
        if self.health>0:
            pygame.draw.line(self.screen, (0, 255, 0), ((self.x - 10), (self.y + 10)), ((self.x + 20*(self.health/self.maxHealth)-10), (self.y + 10)), 7)
    def getDist(self):
        return self.dist
    def getHealth(self):
        return self.health
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
        self.placed = False
        self.sound = pygame.mixer.Sound('laser-zap-90575.mp3')
        self.buffer = 0
    def draw(self):
        pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        self.screen.blit(self.image,(self.x-(self.image.get_width()/2), self.y-(self.image.get_height()/2)))
    def turn(self, angle):
        if angle < 10:
            self.newAngle = math.degrees(angle)
        self.image = pygame.transform.rotate(self.baseImage, self.newAngle)

    def shoot(self):

        pygame.draw.line (self.screen,(255,100,100), (self.x, self.y),
                          (
                              (self.x + (math.cos(self.angle)*300)),
                              (self.y + (math.sin(self.angle)*300))
                          ),
                          20)
        pygame.draw.line(self.screen, (255, 200, 200), (self.x, self.y),
                         (
                             (self.x + (math.cos(self.angle) * 300)),
                             (self.y + (math.sin(self.angle) * 300))
                         ),
                         10)
        if self.buffer <= time.time():
            self.sound.play(1,666)
            self.buffer = time.time()+.666
    def targetEnemy(self, active):   #TARGET FIRST ENEMY
        self.validTarget.clear()
        for enemy in active:
            if distance((self.x,self.y),(enemy.x,enemy.y)) <=300:
                self.validTarget.append(enemy)
        if len(self.validTarget)==0:
            return False
        else:
            self.validTarget.sort(key=lambda t: t.getDist(),reverse=True)


            tar = self.validTarget[0]
            self.targetx = tar.x
            self.targety = tar.y

            if tar.y >= self.y:
                self.angle = math.acos((tar.x-self.x)/(distance((self.x,self.y),(tar.x,tar.y))))
            else:
                self.angle = -1*math.acos((tar.x - self.x) / (distance((self.x, self.y), (tar.x, tar.y))))

            self.turn((self.angle*-1))

            return True
    def hitEnemy(self,enemy):
        hitbox = pygame.draw.line (self.screen,(255,100,100), (self.x, self.y),
                          (
                              (self.x + (math.cos(self.angle)*300)),
                              (self.y + (math.sin(self.angle)*300))
                          ),
                          20)

        return hitbox.collidepoint(enemy.x, enemy.y)
    def touchingMouse(self):
        hitbox = pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        clickposx,clickposy = pygame.mouse.get_pos()
        if  hitbox.collidepoint(clickposx,clickposy):
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 300)
            self.screen.blit(surface,(self.x-300,self.y-300))

class minigunTurret:
    def __init__(self,screen,x,y,angle):
        self.screen =screen
        self.x =x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load('TowerDef_MinigunTurret.png')
        self.baseImage = pygame.image.load('TowerDef_MinigunTurret.png')
        self.validTarget = []
        self.targetnumber =0
        self.targetx=0
        self.targety=0
        self.newAngle = self.angle
        self.placed = False
        self.buffer = 0
        self.sound = pygame.mixer.Sound('bullet.mp3')

    def draw(self):
        pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        self.screen.blit(self.image,(self.x-(self.image.get_width()/2), self.y-(self.image.get_height()/2)))
    def turn(self, angle):
        if angle < 10:
            self.newAngle = math.degrees(angle)
        self.image = pygame.transform.rotate(self.baseImage, self.newAngle)

    def shoot(self):
        if self.buffer <= time.time():
            self.buffer = time.time()+.1
            self.sound.play(1,200)
            pygame.draw.line (self.screen,(255,255,0), (self.x, self.y),
                          (
                              (self.targetx+random.randint(-20,20)),
                              (self.targety+random.randint(-20,20))
                          ),
                          5)

    def targetEnemy(self, active):   #TARGET FIRST ENEMY
        self.validTarget.clear()
        for enemy in active:
            if distance((self.x,self.y),(enemy.x,enemy.y)) <=250:
                self.validTarget.append(enemy)
        if len(self.validTarget)==0:
            return False
        else:
            self.validTarget.sort(key=lambda t: t.getDist(),reverse=True)


            tar = self.validTarget[0]
            self.targetx = tar.x
            self.targety = tar.y

            if tar.y >= self.y:
                self.angle = math.acos((tar.x-self.x)/(distance((self.x,self.y),(tar.x,tar.y))))
            else:
                self.angle = -1*math.acos((tar.x - self.x) / (distance((self.x, self.y), (tar.x, tar.y))))

            self.turn((self.angle*-1))

            return True
    def hitEnemy(self,enemy):
        if self.buffer<=time.time():
            if enemy.x >= self.targetx-7 and enemy.x <= self.targetx+7:
                if enemy.y >= self.targety - 7 and enemy.y <= self.targety + 7:
                    return True
    def touchingMouse(self):
        hitbox = pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        clickposx,clickposy = pygame.mouse.get_pos()
        if  hitbox.collidepoint(clickposx,clickposy):
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 250)
            self.screen.blit(surface,(self.x-300,self.y-300))

class lightningTurret:
    def __init__(self,screen,x,y,angle):
        self.screen =screen
        self.x =x
        self.y = y
        self.angle = angle
        self.image1 = pygame.image.load('TowerDef_LightningReady.png')
        self.baseImage1 = pygame.image.load('TowerDef_LightningReady.png')
        self.image2 = pygame.image.load('TowerDef_LightningFiring.png')
        self.baseImage2 = pygame.image.load('TowerDef_LightningFiring.png')
        self.imagebuffer = 0
        self.validTarget = []
        self.targetnumber =0
        self.targetx=0
        self.targety=0
        self.newAngle = self.angle
        self.placed = False
        self.buffer = 0
        self.level = 1
        self.firing = 0
        self.cooldown =0
        self.damage = 40
        self.buildUp=0
        self.sound=pygame.mixer.Sound('electric_zap_001-6374.mp3')

    def draw(self):
        pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        if self.imagebuffer<=time.time():
            self.screen.blit(self.image1,(self.x-self.image1.get_width()/2,self.y-self.image1.get_height()/2))
        else:
            self.screen.blit(self.image2, (self.x-self.image1.get_width()/2, self.y-self.image1.get_height()/2))

    def turn(self, angle):
        if angle < 10:
            self.newAngle = math.degrees(angle)
        self.image1 = pygame.transform.rotate(self.baseImage1, self.newAngle)
        self.image2 = pygame.transform.rotate(self.baseImage2,self.newAngle)

    def shoot(self):
        if self.buffer <= time.time():
            self.buffer = time.time()+1
            g = random.randint(0, 255)
            for _ in range(20):
                pygame.draw.line(self.screen, (g, g, 255), (self.x, self.y),
                                 (
                                     (self.targetx + random.randint(-20, 20)),
                                     (self.targety + random.randint(-20, 20))
                                 ),
                                 5)
            self.sound.play(1,800)

    def targetEnemy(self, active):   #TARGET FIRST ENEMY
        self.validTarget.clear()
        for enemy in active:
            if distance((self.x,self.y),(enemy.x,enemy.y)) <=300:
                self.validTarget.append(enemy)
        if len(self.validTarget)==0:
            return False
        else:


            self.validTarget.sort(key=lambda t: t.getHealth(),reverse=True)


            tar = self.validTarget[0]
            self.targetx = tar.x
            self.targety = tar.y

            if tar.y >= self.y:
                self.angle = math.acos((tar.x-self.x)/(distance((self.x,self.y),(tar.x,tar.y))))
            else:
                self.angle = -1*math.acos((tar.x - self.x) / (distance((self.x, self.y), (tar.x, tar.y))))

            self.turn((self.angle*-1))

            return True
    def hitEnemy(self,enemy):
        if self.buffer <= time.time():
            if enemy.x >= self.targetx - 7 and enemy.x <= self.targetx + 7:
                if enemy.y >= self.targety - 7 and enemy.y <= self.targety + 7:
                    self.imagebuffer = time.time()+.3
                    return True
    def getDamage(self):
        return self.damage
    def touchingMouse(self):
        hitbox = pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        clickposx,clickposy = pygame.mouse.get_pos()
        if  hitbox.collidepoint(clickposx,clickposy):
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 250)
            self.screen.blit(surface,(self.x-300,self.y-300))

class staticTurret:
    def __init__(self,screen,x,y,angle):
        self.screen =screen
        self.x =x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load('TowerDef_StaticTurret.png')
        self.baseImage = pygame.image.load('TowerDef_StaticTurret.png')
        self.validTarget = []
        self.targetnumber =0
        self.targetx=0
        self.targety=0
        self.newAngle = self.angle
        self.placed = False
        self.sound = pygame.mixer.Sound('laser-zap-90575.mp3')
        self.buffer = 0
    def draw(self):
        pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),24)
        self.screen.blit(self.image,(self.x-(self.image.get_width()/2), self.y-(self.image.get_height()/2)))
    def turn(self, angle):
        if angle < 10:
            self.newAngle = math.degrees(angle)
        self.image = pygame.transform.rotate(self.baseImage, self.newAngle)


    def targetEnemy(self, active):
        self.validTarget.clear()
        for enemy in active:
            if distance((self.x,self.y),(enemy.x,enemy.y)) <=125:
                self.validTarget.append(enemy)
        if len(self.validTarget)==0:
            return False
        else:
            return True
    def hitEnemy(self,enemy):
        surface = pygame.Surface((250, 250), pygame.SRCALPHA)
        hitbox = pygame.draw.circle(surface,(100,100,225), (self.x,self.y),125,150)
        self.screen.blit(surface,(self.x-125,self.y-125))
        return hitbox.collidepoint(enemy.x, enemy.y)

    def touchingMouse(self):
        hitbox = pygame.draw.circle(self.screen,(155,155,155),(self.x, self.y),20)
        clickposx,clickposy = pygame.mouse.get_pos()
        if  hitbox.collidepoint(clickposx,clickposy):
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 125)
            self.screen.blit(surface,(self.x-300,self.y-300))




class turretLists():
    def __init__(self,screen):
        self.screen = screen
        self.staticTurrets = []
        self.beamTurrets = []
        self.lightningTurrets = []
        self.minigunTurrets = []
    def placeBeam(self,x,y):
        beam = beamTurret(self.screen,x,y,0)
        self.beamTurrets.append(beam)
    def placeMinigun(self,x,y):
        mini = minigunTurret(self.screen,x,y,0)
        self.minigunTurrets.append(mini)
    def placeLightning(self,x,y):
        light = lightningTurret(self.screen,x,y,0)
        self.lightningTurrets.append(light)
    def placeStatic(self,x,y):
        static = staticTurret(self.screen,x,y,0)
        self.staticTurrets.append(static)


def updateMouse():
    if pygame.mouse.get_pressed()[0]:
        return True
    else:
        return False
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
        self.lastspawntime = 0
    def spawns(self,tim, health,speed,color):
        time.time()
        f = 0
        if time.time() - self.lastspawntime >= tim:
            Enemy = enemy(self.screen, color, 5, 200, 50, 5, 0, 50, speed)
            self.wavespawn.append(Enemy)
            Enemy.health = health
            Enemy.maxHealth = health
            self.lastspawntime = time.time()
            return True
        return False


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
        self.buy4x = 900
        self.buyy = 550
        self.image1 = pygame.image.load('TowerDef_BeamTurret.png')
        self.image2 = pygame.image.load('TowerDef_MinigunTurret.png')
        self.image3 = pygame.image.load('TowerDef_LightningReady.png')
        self.image4 = pygame.image.load('TowerDef_StaticTurret.png')
    def draw(self,lives,money,wave):
        pygame.draw.rect(self.screen, (50,50,50),(0,525,1080,150))
        pygame.draw.circle(self.screen,(125,125,125),(self.buy1x,self.buyy),24)
        pygame.draw.circle(self.screen, (125, 125, 125), (self.buy2x, self.buyy), 24)
        pygame.draw.circle(self.screen, (125, 125, 125), (self.buy3x, self.buyy), 24)
        pygame.draw.circle(self.screen, (125, 125, 125), (self.buy4x, self.buyy), 24)
        self.screen.blit(self.image1,(self.buy1x-(self.image1.get_width()/2), self.buyy-(self.image1.get_height()/2)))
        self.screen.blit(self.image2,
                         (self.buy2x - (self.image2.get_width() / 2), self.buyy - (self.image2.get_height() / 2)))
        self.screen.blit(self.image3,(self.buy3x - (self.image3.get_width() / 2), self.buyy - (self.image3.get_height() / 2)))
        self.screen.blit(self.image4,
                         (self.buy4x - (self.image4.get_width() / 2), self.buyy - (self.image4.get_height() / 2)))
        font = pygame.font.SysFont("Arial", 20)
        pygame.draw.rect(self.screen, (155, 155, 155),(0,0,125,75))

        str1 = "Lives: "+str(lives)
        str2 = "Money: "+str(round(money))
        str3 = "Wave: "+str(wave)
        text1 = font.render(str1,True,(255,255,255))
        text2 = font.render(str2,True,(255,255,255))
        text3 = font.render(str3,True,(255,255,255))
        self.screen.blit(text1, (0,0))
        self.screen.blit(text2, (0,25))
        self.screen.blit(text3, (0,50))
        text4 = font.render("Cost: 750",True,(255,255,255))
        self.screen.blit(text4, (67,575))
        text5 = font.render("Cost: 500", True, (255, 255, 255))
        self.screen.blit(text5, (367, 575))
        text6 = font.render("Cost: 600", True, (255, 255, 255))
        self.screen.blit(text6, (667, 575))
        text7 = font.render("Cost: 300", True, (255, 255, 255))
        self.screen.blit(text7, (867, 575))
    #def purchase(self,clickposx,clickposy,mouseDown,money):
    #    if mouseDown: #boolean
    #        if clickposy >= self.buyy-10 and clickposy <= self.buyy +10:
    #            if clickposx >= self.buy1x-10 and clickposx <= self.buy1x+10:
    #                image1 = pygame.image.load('TowerDef_BeamTurret - Copy - Copy.png')
    #                font = pygame.font.SysFont("Arial",30)
    #
    #                text = font.render("click on desired position, or back to the shop to deselect",True,(0,0,0))
    #                buffer = time.time() + 1
    #                while mouseDown and buffer>=time.time():
    #                    pygame.draw.circle(self.screen, (155,155,155, 100), (clickposx, clickposy), 20)
    #                    self.screen.blit(image1,(clickposx,clickposy))
    #                    self.screen.blit(text,(500,0))
    #                    mouseDown = self.updateMouse()
    #                    pygame.display.update()





class path:
    def __init__(self, screen):
        self.screen = screen
    def draw(self):
        pygame.draw.line(self.screen, (90, 140, 60), (0, 200), (500, 200), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (475, 180), (475, 500), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (475, 475), (725, 475), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (700, 475), (700, 176), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (700, 200), (1025, 200), 50)
        pygame.draw.line(self.screen, (90, 140, 60), (1000, 200), (1000, 0), 50)
    def collision(self,point):
        hitbox1 =  pygame.draw.line(self.screen, (90, 140, 60), (0, 200), (500, 200), 50)
        hitbox2 =  pygame.draw.line(self.screen, (90, 140, 60), (475, 180), (475, 500), 50)
        hitbox3 =  pygame.draw.line(self.screen, (90, 140, 60), (475, 475), (725, 475), 50)
        hitbox4 =  pygame.draw.line(self.screen, (90, 140, 60), (700, 475), (700, 176), 50)
        hitbox5 =  pygame.draw.line(self.screen, (90, 140, 60), (700, 200), (1025, 200), 50)
        hitbox6 =  pygame.draw.line(self.screen, (90, 140, 60), (1000, 200), (1000, 0), 50)
        if hitbox1.collidepoint(point.x,point.y):
            return 1
        elif hitbox2.collidepoint(point.x,point.y):
            return 1
        elif hitbox3.collidepoint(point.x,point.y):
            return 1
        elif hitbox4.collidepoint(point.x,point.y):
            return 1
        elif hitbox5.collidepoint(point.x,point.y):
            return 1
        elif hitbox6.collidepoint(point.x,point.y):
            return 1
        else:
            return 0














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
    totalSpawns = 0
    last_wave_time = 0
    enemies_left = 0
    enemies_left2 = 0
    mouseDown = False
    placingTower3=False
    lives = 500
    money = 750
    selectSound = pygame.mixer.Sound('clicking-interface-select-201946.mp3')
    placeSound = pygame.mixer.Sound('place_object.mp3')

    targetpurchase =0
    UI = ui(screen)
    towers = []
    listT = turretLists(screen)
    spawns = waveSpawn(screen, gamestate)
    spawns2 = waveSpawn(screen, gamestate)
    placingTower4 = False
    activeEnemies = spawns.getList()
    #test = beamTurret(screen, 500, 300, 0.0)
    #my_enemy = enemy(screen, (255, 255, 0), 5, 200, 50, 0, 0)

    beamTurrets = []
    placingTower1 = False
    placingTower2 = False
    wave_delay = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)



        # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((75, 155, 75))

        PTH.draw()



        #spawns.spawns(4,50)

        activeEnemies = spawns.getList()
        if enemies_left<=0:
            gamestate = False
        else:
            gamestate = True
        spawns.updateState(gamestate)
        spawns2.updateState(gamestate)
        #if test.targetEnemy(activeEnemies):
        #    test.shoot()
        for enemy1 in activeEnemies:
            enemy1.move()
            for beam1 in listT.beamTurrets:
                if distance((enemy1.x, enemy1.y),(beam1.x,beam1.y))<300:
                    if beam1.hitEnemy(enemy1):
                        money += enemy1.damage(.25) / waves
            for mini1 in listT.minigunTurrets:
                if distance((enemy1.x, enemy1.y),(mini1.x,mini1.y))<250:
                    if mini1.hitEnemy(enemy1):
                        money += enemy1.damage(2) / waves
            for light1 in listT.lightningTurrets:
                if distance((enemy1.x, enemy1.y),(light1.x,light1.y))<300:
                    if light1.hitEnemy(enemy1):
                        selectSound.play(10)
                        money += enemy1.damage(light1.getDamage()) / waves
            f = 0
            for static1 in listT.staticTurrets:
                if distance((enemy1.x,enemy1.y),(static1.x,static1.y))<=125:
                    f+=1
                if f == 0:
                    enemy1.updateSlowed(False)
                else:
                    enemy1.updateSlowed(True)
            if enemy1.offscreen():
                activeEnemies.remove(enemy1)
                lives -= enemy1.offscreen2()

            if enemy1.deathCheck():
                money+=enemy1.deathCheck2()
                activeEnemies.remove(enemy1)

            enemy1.draw()
        key = pygame.key.get_pressed()
        #test.touchingMouse()
        for beam1 in listT.beamTurrets:
            beam1.touchingMouse()
            if beam1.targetEnemy(activeEnemies):
                beam1.shoot()
            beam1.draw()
        for mini1 in listT.minigunTurrets:
            mini1.touchingMouse()
            if mini1.targetEnemy(activeEnemies):
                mini1.shoot()
            mini1.draw()
        for light1 in listT.lightningTurrets:
            light1.touchingMouse()
            if light1.targetEnemy(activeEnemies):
                light1.shoot()
            light1.draw()
        for static1 in listT.staticTurrets:
            static1.touchingMouse()
            static1.draw()

        if time.time() - last_wave_time > wave_delay and enemies_left <= 0:
            waves +=1
            money += 100+(125*waves)
            last_wave_time = time.time()
            enemies_left = 10
            if waves == 1:
                enemies_left = 5
            elif waves == 2:
                enemies_left = 10
            elif waves == 3:
                enemies_left = 15
            elif waves == 4:
                enemies_left = 20
            elif waves == 5:
                enemies_left = 25
            elif waves == 6:
                enemies_left = 30
                wave_delay = 5
            elif waves == 7:
                enemies_left = 35
                wave_delay = 3
            elif waves == 8:
                enemies_left = 40
            elif waves == 9:
                enemies_left = 45
            elif waves == 10:
                enemies_left = 1
                wave_delay = 20
            elif waves == 11:
                enemies_left = 50
                wave_delay = 3
                # money += enemy1.damage(.25) / (waves * (3))
            elif waves == 12:
                enemies_left = 55
                wave_delay = 5
            elif waves == 13:
                enemies_left = 60
                wave_delay = 3
            elif waves == 14:
                enemies_left = 65
            elif waves == 15:
                enemies_left = 3
                wave_delay = 20
            elif waves == 16:
                enemies_left = 70
                wave_delay = 3
            elif waves == 17:
                enemies_left = 75

        if waves == 1 and enemies_left > 0:
            if spawns.spawns(2, 10, 2, (20, 200, 20)):
                enemies_left -= 1

        if waves == 2 and enemies_left > 0:
            if spawns.spawns(2, 15, 4, (20, 255, 100)):
                enemies_left -= 1

        if waves == 3 and enemies_left > 0:
            if spawns.spawns(1, 35, 4, (20, 100, 20)):
                enemies_left -= 1

        if waves == 4 and enemies_left > 0:
            if spawns.spawns(1, 55, 3, (20, 200, 20)):
                enemies_left -= 1

        if waves == 5 and enemies_left > 0:
            if spawns.spawns(.8, 75, 4, (20, 200, 200)):
                enemies_left -= 1

        if waves == 6 and enemies_left > 0:
            if spawns.spawns(.8, 190, 2, (20, 50, 200)):
                enemies_left -= 1

        if waves == 7 and enemies_left > 0:
            if spawns.spawns(.5, 50, 8, (20, 240, 10)):
                enemies_left -= 1

        if waves == 8 and enemies_left > 0:
            if spawns.spawns(.7, 230, 3, (200, 100, 20)):
                enemies_left -= 1

        if waves == 9 and enemies_left > 0:
            if spawns.spawns(.5, 140, 7, (0, 250, 100)):
                enemies_left -= 1

        if waves == 10 and enemies_left > 0:
            if spawns.spawns(1, 3200, 1, (255, 10, 10)):
                enemies_left -= 1

        if waves == 11 and enemies_left > 0:
            if spawns.spawns(.3, 200, 5, (100, 200, 50)):
                enemies_left -= 1

        if waves == 12 and enemies_left > 0:
            if spawns.spawns(.4, 370, 2, (225, 225, 0)):
                enemies_left -= 1

        if waves == 13 and enemies_left > 0:
            if spawns.spawns(.2, 100, 9, (0, 225, 20)):
                enemies_left -= 1

        if waves == 14 and enemies_left > 0:
            if spawns.spawns(.7, 380, 4, (40, 70, 200)):
                enemies_left -= 1

        if waves == 15 and enemies_left > 0:
            if spawns.spawns(1, 4500, 1, (255, 180, 90)):
                enemies_left -= 1

        if waves == 16 and enemies_left > 0:
            if spawns.spawns(.1, 140, 8, (0,225,80)):
                enemies_left -= 1

        if waves == 17 and enemies_left > 0:
            if spawns.spawns(.8, 450, 3, (50, 0, 225)):
                enemies_left -= 1

        if waves == 18 and enemies_left > 0:
            if spawns.spawns(1.5, 800, 1.5, (225, 140, 20)):
                enemies_left -= 1

        if waves == 19 and enemies_left > 0:
            if spawns.spawns(.7, 200, 7, (0, 255, 0)):
                enemies_left -= 1

        #if waves == 20

        if lives <= 0:
            break

        UI.draw(lives,money,waves)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickposx,clickposy = event.pos

            mouseDown = True
            if clickposy >= 530:
                if mouseDown: #boolean
                    selectSound.play(1)
                    if money >=750:
                            if clickposy >= 540 and clickposy <= 560:
                                if clickposx >= 85 and clickposx <= 115:
                                    image1 = pygame.image.load('TowerDef_BeamTurret - Copy - Copy.png')
                                    font = pygame.font.SysFont("Arial",30)

                                    text = font.render("click on desired position, or back to the shop to deselect",True,(0,0,0))
                                    buffer = time.time() + .2
                                    placingTower1 = True
                    if money >= 500:
                        if clickposy >= 540 and clickposy <= 560:
                                    if clickposx >=385 and clickposx <=415:
                                        image2 = pygame.image.load('TowerDef_MinigunTurret.png')
                                        font = pygame.font.SysFont("Arial", 30)

                                        text = font.render("click on desired position, or back to the shop to deselect",
                                                       True, (0, 0, 0))
                                        buffer = time.time() + .2
                                        placingTower2 = True
                    if money >= 600:
                        if clickposy >= 540 and clickposy <= 560:
                            if clickposx >= 685 and clickposx <= 715:
                                image3 = pygame.image.load('TowerDef_LightningReady.png')
                                font = pygame.font.SysFont("Arial", 30)

                                text = font.render("click on desired position, or back to the shop to deselect",
                                                   True, (0, 0, 0))
                                buffer = time.time() + .2
                                placingTower3 = True
                    if money >= 300:
                        if clickposy >= 540 and clickposy <= 560:
                            if clickposx >= 885 and clickposx <= 915:
                                image4 = pygame.image.load('TowerDef_StaticTurret.png')
                                font = pygame.font.SysFont("Arial", 30)

                                text = font.render("click on desired position, or back to the shop to deselect",
                                                   True, (0, 0, 0))
                                buffer = time.time() + .2
                                placingTower4 = True

        if placingTower1:
            pygame.draw.circle(screen, (155, 155, 155), pygame.mouse.get_pos(), 20)
            x,y = pygame.mouse.get_pos()
            box = pygame.draw.rect(screen, (155, 155, 155), (x - 10, y - 10, 20, 20))
            screen.blit(image1, (x-image1.get_width()/2,y-image1.get_height()/2))
            screen.blit(text, (250, 0))
            mouseDown = updateMouse()
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 300)
            screen.blit(surface, (x - 300, y - 300))

            a = 0
            if mouseDown and buffer <= time.time():
                placingTower1 = False
                if y <= 525:
                    if len(listT.beamTurrets) > 0:
                        for beam1 in listT.beamTurrets:
                            if (box.collidepoint(beam1.x, beam1.y)):
                                a += 1
                    if len(listT.minigunTurrets) > 0:
                        for mini1 in listT.minigunTurrets:
                            if (box.collidepoint(mini1.x, mini1.y)):
                                a += 1
                    if len(listT.lightningTurrets) > 0:
                        for light1 in listT.lightningTurrets:
                            if box.collidepoint(light1.x, light1.y):
                                a += 1
                    if len(listT.staticTurrets) > 0:
                        for static1 in listT.staticTurrets:
                            if box.collidepoint(static1.x, static1.y):
                                a += 1
                    a+=PTH.collision(box)
                    if a == 0:
                        listT.placeBeam(x,y)
                        money-=750
                        placeSound.play(1)
        if placingTower2:
            pygame.draw.circle(screen, (155, 155, 155), pygame.mouse.get_pos(), 20)
            x, y = pygame.mouse.get_pos()
            box = pygame.draw.rect(screen, (155, 155, 155), (x - 10, y - 10, 20, 20))
            screen.blit(image2, (x - image2.get_width() / 2, y - image2.get_height() / 2))
            screen.blit(text, (250, 0))
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 250)
            screen.blit(surface, (x - 300, y - 300))

            a = 0
            mouseDown = updateMouse()
            if mouseDown and buffer <= time.time():
                placingTower2 = False
                if y <=525:
                    if len(listT.beamTurrets)>0:
                        for beam1 in listT.beamTurrets:
                            if (box.collidepoint(beam1.x, beam1.y)):
                                a +=1
                    if len(listT.minigunTurrets)>0:

                        for mini1 in listT.minigunTurrets:
                            if (box.collidepoint(mini1.x, mini1.y)):
                                a +=1
                    if len(listT.lightningTurrets) > 0:
                        for light1 in listT.lightningTurrets:
                            if box.collidepoint(light1.x, light1.y):
                                a += 1
                    if len(listT.staticTurrets) > 0:
                        for static1 in listT.staticTurrets:
                            if box.collidepoint(static1.x, static1.y):
                                a += 1
                    a += PTH.collision(box)
                    if a == 0:
                        listT.placeMinigun(x, y)
                        money -= 500
                        placeSound.play(1)
        if placingTower3:
            pygame.draw.circle(screen, (155, 155, 155), pygame.mouse.get_pos(), 20)
            x, y = pygame.mouse.get_pos()
            box = pygame.draw.rect(screen, (155, 155, 155), (x - 10, y - 10, 20, 20))
            screen.blit(image3, (x - image3.get_width() / 2, y - image3.get_height() / 2))
            screen.blit(text, (250, 0))
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 250)
            screen.blit(surface, (x - 300, y - 300))

            a = 0
            mouseDown = updateMouse()
            if mouseDown and buffer <= time.time():
                placingTower3 = False
                if y <= 525:
                        if len(listT.beamTurrets) > 0:
                            for beam1 in listT.beamTurrets:
                                if (box.collidepoint(beam1.x, beam1.y)):
                                    a += 1
                        if len(listT.minigunTurrets) > 0:
                            for mini1 in listT.minigunTurrets:
                                if (box.collidepoint(mini1.x, mini1.y)):
                                    a += 1
                        if len(listT.lightningTurrets)>0:
                            for light1 in listT.lightningTurrets:
                                if box.collidepoint(light1.x,light1.y):
                                    a+=1
                        if len(listT.staticTurrets) > 0:
                            for static1 in listT.staticTurrets:
                                if box.collidepoint(static1.x, static1.y):
                                    a += 1

                        a += PTH.collision(box)
                        if a == 0:
                            listT.placeLightning(x, y)
                            money -= 600
                        placeSound.play(1)
        if placingTower4:
            pygame.draw.circle(screen, (155, 155, 155), pygame.mouse.get_pos(), 20)
            x, y = pygame.mouse.get_pos()
            box = pygame.draw.rect(screen, (155, 155, 155), (x - 10, y - 10, 20, 20))
            screen.blit(image4, (x - image4.get_width() / 2, y - image4.get_height() / 2))
            screen.blit(text, (250, 0))
            mouseDown = updateMouse()
            surface = pygame.Surface((600, 600), pygame.SRCALPHA)
            pygame.draw.circle(surface, (200, 200, 200, 100), (300, 300), 125)
            screen.blit(surface, (x - 300, y - 300))

            a = 0
            if mouseDown and buffer <= time.time():
                placingTower4 = False
                if y <= 525:
                    if len(listT.beamTurrets) > 0:
                        for beam1 in listT.beamTurrets:
                            if (box.collidepoint(beam1.x, beam1.y)):
                                a += 1
                    if len(listT.minigunTurrets) > 0:
                        for mini1 in listT.minigunTurrets:
                            if (box.collidepoint(mini1.x, mini1.y)):
                                a += 1
                    if len(listT.lightningTurrets) > 0:
                        for light1 in listT.lightningTurrets:
                            if box.collidepoint(light1.x, light1.y):
                                a += 1
                    if len(listT.staticTurrets) > 0:
                        for static1 in listT.staticTurrets:
                            if box.collidepoint(static1.x, static1.y):
                                a += 1
                    a += PTH.collision(box)
                    if a == 0:
                        listT.placeStatic(x, y)
                        money -= 300
                        placeSound.play(1)

                #append beamTurret here


        #    #TODO: MAKE UNIQUE WAVES

        #test.draw()


        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()


main()





