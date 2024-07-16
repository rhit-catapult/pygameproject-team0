#while len(self.validTarget) > 1:
#    for enemy in self.validTarget:
#        self.validTarget.remove(enemy)
#    self.targetnumber += 1
#if len(self.validTarget) <= 0:
#    for enemy in active:
#        if distance((self.x, self.y), (enemy.x, enemy.y)) <= 300 and enemy.dist <= self.targetnumber:
#            self.validTarget.append(enemy)
#    r = random.randint(0, (len(self.validTarget) - 1))
#    tar = self.validTarget[r]
#    self.targetx = tar.x
#    self.targety = tar.y
#    self.angle = math.atan(tar.y / tar.x)
#    self.turn(self.angle)
#    print((self.targetx, self.targety))
#    if distance((self.x, self.y), (tar.x, tar.y)) > 300 or tar.health <= 0:
#        tar = None
#        self.targetnumber = 0
#        self.targety = None
#        self.targetx = None
#        return False
#    self.targetnumber = 0
#    return True







