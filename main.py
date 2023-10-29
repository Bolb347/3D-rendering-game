##credit goes to Lord-McSweeny for explaining the trigonometric functions used in ray calculations based on angles
##rest of the code is mine

import pygame, math, sys
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((400, 800))
resolution = 1

class Block:
    blockList = []
   
    def __init__(self, x, y, width, height, color = "white"):
        self.x = x
        self.y = y+400
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
   
        Block.blockList.append(self)
       
    def draw(self):
        pygame.draw.rect(screen, self.color, self.hitbox)

class Player:
    def __init__(self, x, y, angle = 0, vd = 500):
        self.x = x
        self.y = y+400
        self.angle = angle
        self.vd = vd

    def draw(self):
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
   
    Ray.rayList.append(self)
 
  def cast(self):
    broken = False
    while broken == False:
      if self.length <= self.maxLength:
        if self.angle != 90 or self.angle != 270:
          self.x += self.modx
        if self.angle != 180:
          self.y += self.mody
        self.length += 1
        #pygame.draw.circle(screen, "red", (self.x, self.y), 1)
        for block in Block.blockList:
          if block.hitbox.collidepoint(self.x, self.y):
            self.distance = math.sqrt((player.x-self.x)*(player.x-self.x)+(player.y-self.y)*(player.y-self.y))
            self.color = block.color
            broken = True
      else:
        broken = True
    Ray.rayList.remove(self)


def castSurface(ray):
  if ray.distance != None and ray.color != None and ray.distance != 0:
    pygame.draw.line(screen, ray.color, (ray.idx*((400/60)*resolution), 200-(5000/ray.distance)), (ray.idx*((400/60)*resolution), 200+(5000/ray.distance)), 7)

def renderGround(x, y, width, height, color):
  pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

def makeBlock(x1, y1, width, height, r = 245, g = 245, b = 245, orientation = "vertical"):
  if r > 245:
    r = 245
  if g > 245:
    g = 245
  if b > 245:
    b = 245
  Block(x1, y1, width, height, (r, g, b))
  if orientation == "vertical":
    Block(x1-1, y1, 1, height, (r+10, g+10, b+10))
    Block(x1+width, y1, 1, height, (r+10, g+10, b+10))
  elif orientation == "horizontal":
    Block(x1, y1-1, width, 1, (r+10, g+10, b+10))
    Block(x1, y1+height, width, 1, (r+10, g+10, b+10))
  else:
    print("orientation not supported(try vertical/horizontal)")
  

player = Player(200, 200)


makeBlock(350, 150, 400, 250, 255, 0, 0)
makeBlock(300, 100, 310, 110, 0, 255, 0, "horizontal")
makeBlock(100, 0, 150, 150, 0, 0, 255)
makeBlock(0, 0, 10, 400)
makeBlock(0, 0, 400, 10)
makeBlock(390, 0, 10, 400)
makeBlock(0, 390, 400, 10)


while True:
    pygame.event.get()
    screen.fill("black")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.angle += 1
    if keys[pygame.K_LEFT]:
        player.angle -= 1
    if keys[pygame.K_UP]:
        player.x += math.cos(math.radians(player.angle))
        player.y += math.sin(math.radians(player.angle))
        for block in Block.blockList:
          if block.hitbox.collidepoint(player.x, player.y):
            player.x -= math.cos(math.radians(player.angle))
            player.y -= math.sin(math.radians(player.angle))
    if keys[pygame.K_DOWN]:
        player.x -= math.cos(math.radians(player.angle))
        player.y -= math.sin(math.radians(player.angle))
        for block in Block.blockList:
          if block.hitbox.collidepoint(player.x, player.y):
            player.x += math.cos(math.radians(player.angle))
            player.y += math.sin(math.radians(player.angle))
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
   
 
    for ray in range(math.ceil(60/resolution)):
        Ray((ray*resolution-30)+player.angle, player.vd, player.x, player.y, ray)
    renderGround(0, 200, 400, 200, (200, 100, 0))
    for ray in Ray.rayList:
        ray.cast()
        castSurface(ray)
    for block in Block.blockList:
        block.draw()

    player.draw()

    pygame.display.update()
    clock.tick(60)
