import pygame, math, sys
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((400, 400))
resolution = 1
moveSpeed = 2

running = True
scene = "Game"

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
    def __init__(self, x, y, angle = 0, vd = 500):
        self.x = x
        self.y = y
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
        self.surface = None

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
                for obj in tempList:
                    if obj.hitbox.collidepoint(self.x, self.y):
                        self.distance = math.sqrt((player.x-self.x)*(player.x-self.x)+(player.y-self.y)*(player.y-self.y))
                        self.surface = obj.surface
                        tempList.remove(obj)
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
  
  def __init__(self, x, y, img, boxw, boxh, speed = 1, damage = 1):
    super().__init__(x, y, img, boxw, boxh)
    self.speed = speed
    self.damage = damage
    
    Enemy.enemyList.append(self)
  
  def move(self):
    self.hitbox = pygame.Rect(self.x-self.boxw/2, self.y-self.boxw/2, self.boxw, self.boxh)
    self.x -= (self.x-player.x)/100
    self.y -= (self.y-player.y)/100
    for block in Block.blockList:
            if block.hitbox.collidepoint(self.x, self.y):
                self.x += (self.x-player.x)/100
                self.y += (self.y-player.y)/100
    


def castSurface(ray):
    if ray.distance != None and ray.distance != 0 and ray.color != None:
        pygame.draw.line(screen, ray.color, (ray.idx*((400/60)*resolution), 200-(5000/ray.distance)), (ray.idx*((400/60)*resolution), 200+(5000/ray.distance)), 14)
    if ray.distance != None and ray.distance != 0 and ray.surface != None:
        pendingDrawings.append(ray)
 
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
        print("orientation not supported(try 'vertical'/'horizontal')")
 

player = Player(200, 200)


makeBlock(350, 150, 400, 250, 255, 0, 0)
makeBlock(300, 100, 310, 110, 0, 255, 0, "horizontal")
makeBlock(100, 0, 150, 150, 0, 0, 255)
makeBlock(0, 0, 10, 400)
makeBlock(0, 0, 400, 10)
makeBlock(390, 0, 10, 400)
makeBlock(0, 390, 400, 10)
Enemy(200, 170, "obj.png", 10, 10) #need to change name to a jpg or gif in your directory

while running == True:
    tempList = []
    for obj in Obj.objList:
        tempList.append(obj)
    pendingDrawings = []
    events = pygame.event.get()
    screen.fill("black")

    keys = pygame.key.get_pressed()
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
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if scene == "Game":
                scene = "Map"
            elif scene == "Map":
                scene = "Game"


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
