import pygame, math, sys
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
lastColor = None

screen = pygame.display.set_mode((400, 400))
resolution = 1
moveSpeed = 2

font = pygame.font.SysFont("arial", 20)

running = True
scene = "Title"

class Block:
    blockList = []

    def __init__(self, x, y, width, height, color = "white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color

        Block.blockList.append(self)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.hitbox)

class Player:
    def __init__(self, x, y, angle = 0, vd = 500, maxHealth = 10, hwidth = 10, hlength = 10):
        self.x = x
        self.y = y
        self.angle = angle
        self.vd = vd
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.hwidth = hwidth
        self.hlength = hlength
        self.hitbox = pygame.Rect(x-5, y-5, hwidth, hlength)

    def draw(self):
        self.hitbox = pygame.Rect(self.x-5, self.y-5, self.hwidth, self.hlength)
        pygame.draw.circle(screen, "brown", (self.x, self.y), 5)
        pygame.draw.line(screen, "gray", (self.x, self.y), (self.x + math.cos(math.radians(self.angle))*10, self.y + math.sin(math.radians(self.angle))*10))


class Ray:
    rayList = []

    def __init__(self, angle, maxLength, initialX, initialY, idx):
        self.x = initialX
        self.y = initialY
        self.angle = angle
        self.maxLength = maxLength
        self.length = 0
        self.modx = math.cos(math.radians(self.angle))
        self.mody = math.sin(math.radians(self.angle))
        self.idx = idx
        self.distance = None
        self.color = None
        self.surface = None

        Ray.rayList.append(self)

    def cast(self):
        global lastColor
        broken = False
        while broken == False:
            if self.length <= self.maxLength:
                if self.angle != 90 or self.angle != 270:
                    self.x += self.modx
                if self.angle != 180:
                    self.y += self.mody
                self.length += 1
                if scene == "Map":
                    pygame.draw.circle(screen, "gray", (self.x, self.y), 1)
                for block in Block.blockList:
                    if block.hitbox.collidepoint(self.x, self.y):
                        self.distance = math.sqrt((player.x-self.x)*(player.x-self.x)+(player.y-self.y)*(player.y-self.y))
                        self.color = block.color
                        lastColor = block.color
                        broken = True
                for obj in tempList:
                    if obj.hitbox.collidepoint(self.x, self.y):
                        self.distance = math.sqrt((player.x-self.x)*(player.x-self.x)+(player.y-self.y)*(player.y-self.y))
                        self.surface = obj.surface
                        ray1 = Ray(ray.angle, ray.maxLength, ray.x, ray.y, ray.idx)
                        ray1.x = ray.x
                        ray1.y = ray.y
                        ray1.color = lastColor
                        tempList.remove(obj)
                        broken = True
                for projectile in tempList2:
                    if projectile.hitbox.collidepoint(self.x, self.y):
                        self.distance = math.sqrt((player.x-self.x)*(player.x-self.x)+(player.y-self.y)*(player.y-self.y))
                        ray1 = Ray(ray.angle, ray.maxLength, ray.x, ray.y, ray.idx)
                        ray1.x = ray.x
                        ray1.y = ray.y
                        ray1.color = lastColor
                        tempList.remove(projectile)
                        broken = True
            else:
                broken = True
        Ray.rayList.remove(self)

class Obj:
    objList = []

    def __init__(self, x, y, img, boxw, boxh):
        self.x = x
        self.y = y
        self.img = img
        self.boxw = boxw
        self.boxh = boxh
        self.hitbox = pygame.Rect(x-boxw/2, y-boxw/2, boxw, boxh)
        if img != None:
            self.surface = pygame.image.load(img)

        Obj.objList.append(self)

    def draw(self):
        pygame.draw.circle(screen, "pink", (self.x, self.y), 5)
        

class Enemy(Obj):
  enemyList = []
  
  def __init__(self, x, y, img, boxw, boxh, damage = 1, speed = 1, ran = 50, fireSpeed = 50, health = 5):
    super().__init__(x, y, img, boxw, boxh)
    self.damage = damage
    self.xspeed = 1
    self.yspeed = 1
    self.speed = speed
    self.distance = 0
    self.ran = ran
    self.fireSpeed = fireSpeed
    self.fireTimer = fireSpeed
    self.health = health
    
    Enemy.enemyList.append(self)
  
  def move(self):
    self.distance = getDistance(self.x, self.y, player.x, player.y)
    if self.distance > self.ran:
        self.xspeed = ((self.x-player.x)/self.distance)*self.speed
        self.yspeed = ((self.y-player.y)/self.distance)*self.speed
        self.hitbox = pygame.Rect(self.x-self.boxw/2, self.y-self.boxw/2, self.boxw, self.boxh)
        self.x -= self.xspeed
        self.y -= self.yspeed
        for block in Block.blockList:
            if block.hitbox.collidepoint(self.x, self.y):
                self.x += self.xspeed
                self.y += self.yspeed
  
  def fire(self):
    self.fireTimer -= 1
    if self.fireTimer <= 0:
      Projectile(self.x, self.y, self.xspeed*2, self.yspeed*2, self.damage, "enemy")
      self.fireTimer = self.fireSpeed



class Projectile:
  projectileList = []
  
  def __init__(self, x, y, xspeed, yspeed, damage, types):
    self.x = x
    self.y = y
    self.xspeed = xspeed
    self.yspeed = yspeed
    self.damage = damage
    self.types = types
    self.hitbox = pygame.Rect(x, y, 5, 5)
    
    Projectile.projectileList.append(self)
  
  def move(self):
    self.x -= self.xspeed
    self.y -= self.yspeed
    self.hitbox = pygame.Rect(self.x, self.y, 5, 5)

    if scene == "Map":
        pygame.draw.circle(screen, "purple", (self.x, self.y), 2)
    
    for block in Block.blockList:
      if block.hitbox.collidepoint(self.x, self.y):
        Projectile.projectileList.remove(self)
        break
      
    if self.types == "enemy":
      if player.hitbox.collidepoint(self.x, self.y):
        player.health -= self.damage
        Projectile.projectileList.remove(self)
    elif self.types == "player":
      for enemy in Enemy.enemyList:
        if enemy.hitbox.collidepoint(self.x, self.y):
          enemy.health -= self.damage
          Projectile.projectileList.remove(self)

def castSurface(ray):
    if ray.distance != None and ray.distance != 0 and ray.color != None:
        pygame.draw.line(screen, ray.color, (ray.idx*((400/60)*resolution), 200-(5000/ray.distance)), (ray.idx*((400/60)*resolution), 200+(5000/ray.distance)), 7)
    if ray.distance != None and ray.distance != 0 and ray.surface != None:
        pendingDrawings.append(ray)
 
def renderGround(x, y, width, height, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

def makeBlock(x1, y1, width, height, r = 245, g = 245, b = 245, orientation = "vertical"):
    if r > 235:
        r = 235
    if g > 235:
        g = 235
    if b > 235:
        b = 235
    Block(x1, y1, width, height, (r, g, b))
    if orientation == "vertical":
        Block(x1-1, y1, 1, height, (r+20, g+20, b+20))
        Block(x1+width, y1, 1, height, (r+20, g+20, b+20))
    elif orientation == "horizontal":
        Block(x1, y1-1, width, 1, (r+20, g+20, b+20))
        Block(x1, y1+height, width, 1, (r+20, g+20, b+20))
    else:
        print("orientation not supported(try 'vertical'/'horizontal')")
 

def getDistance(x1, y1, x2, y2):
  return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))


player = Player(200, 200)


makeBlock(350, 150, 400, 250, 255, 0, 0)
makeBlock(300, 100, 310, 110, 0, 255, 0, "horizontal")
makeBlock(100, 0, 150, 150, 0, 0, 255)
makeBlock(0, 0, 10, 400)
makeBlock(0, 0, 400, 10)
makeBlock(390, 0, 10, 400)
makeBlock(0, 390, 400, 10)
Enemy(200, 170, "square2.png", 10, 10) #need to change name to a jpg or gif in your directory

while running == True:
    tempList = []
    tempList2 = []
    for obj in Obj.objList:
        tempList.append(obj)
    for projectile in Projectile.projectileList:
        tempList2.append(projectile)
    pendingDrawings = []
    events = pygame.event.get()
    screen.fill("black")

    keys = pygame.key.get_pressed()
    if scene == "Game" or scene == "Map":
        if keys[pygame.K_RIGHT]:
            player.angle += 2
        if keys[pygame.K_LEFT]:
            player.angle -= 2
        if keys[pygame.K_UP]:
            player.x += math.cos(math.radians(player.angle))*moveSpeed
            player.y += math.sin(math.radians(player.angle))*moveSpeed
            for block in Block.blockList:
                if block.hitbox.collidepoint(player.x, player.y):
                    player.x -= math.cos(math.radians(player.angle))*moveSpeed
                    player.y -= math.sin(math.radians(player.angle))*moveSpeed
        if keys[pygame.K_DOWN]:
            player.x -= math.cos(math.radians(player.angle))*moveSpeed
            player.y -= math.sin(math.radians(player.angle))*moveSpeed
            for block in Block.blockList:
                if block.hitbox.collidepoint(player.x, player.y):
                    player.x += math.cos(math.radians(player.angle))*moveSpeed
                    player.y += math.sin(math.radians(player.angle))*moveSpeed
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if scene == "Game":
                    scene = "Map"
                elif scene == "Map":
                    scene = "Game"
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    if scene == "Title":
        text = font.render("Doom V0.01", True, "white")
        screen.blit(text, (100, 100))
        text = font.render("Press 'SPACE' to start", True, "white")
        screen.blit(text, (120, 125))
        text = font.render("Press 'H' for help", True, "white")
        screen.blit(text, (120, 150))
        text = font.render("Made by Bolb347", True, "white")
        screen.blit(text, (0, 350))

        if keys[pygame.K_SPACE]:
            scene = "Game"
        if keys[pygame.K_h]:
            scene = "Help"

    if scene == "Help":
        text = font.render("Controls:", True, "white")
        screen.blit(text, (100, 100))
        text = font.render("Left Arrow/Right Arrow to turn", True, "white")
        screen.blit(text, (120, 125))
        text = font.render("Up Arrow/Down Arrow to move", True, "white")
        screen.blit(text, (120, 150))
        text = font.render("Space is to switch from game to map", True, "white")
        screen.blit(text, (120, 175))
        text = font.render("Press 'T' to go back to title screen", True, "white")
        screen.blit(text, (120, 200))

        if keys[pygame.K_t]:
            scene = "Title"

    for ray in range(math.ceil(60/resolution)):
        Ray((ray*resolution-30)+player.angle, player.vd, player.x, player.y, ray)
    if scene == "Game":
        renderGround(0, 200, 400, 200, (200, 100, 0))
    for ray in Ray.rayList:
        ray.cast()
        if scene == "Game":
            castSurface(ray)
    for enemy in Enemy.enemyList:
        enemy.move()
        enemy.fire()
    for projectile in Projectile.projectileList:
        projectile.move()
    if scene == "Map":
        for block in Block.blockList:
            block.draw()
        for obj in Obj.objList:
            obj.draw()

    if scene == "Game":
        for ray in pendingDrawings:
            ray.surface = pygame.transform.scale(ray.surface, (5000/ray.distance, 5000/ray.distance))
            screen.blit(ray.surface, (ray.idx*((400/60)*resolution), 200))

    if scene == "Map":
        player.draw()
    
    pygame.display.update()
    clock.tick(60)
