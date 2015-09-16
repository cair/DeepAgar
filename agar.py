import pygame,random,math

pygame.init()
colors_players = [(37,7,255),(35,183,253),(48,254,241),(19,79,251),(255,7,230),(255,7,23),(6,254,13)]
colors_cells = [(80,252,54),(36,244,255),(243,31,46),(4,39,243),(254,6,178),(255,211,7),(216,6,254),(145,255,7),(7,255,182),(255,6,86),(147,7,255)]
colors_viruses = [(66,254,71)]
screen_width, screen_height = (500,500)
surface = pygame.display.set_mode((screen_width,screen_height))
t_surface = pygame.Surface((95,25),pygame.SRCALPHA) #transparent rect for score
t_lb_surface = pygame.Surface((155,278),pygame.SRCALPHA) #transparent rect for leaderboard
t_surface.fill((50,50,50,80))
t_lb_surface.fill((50,50,50,80))
pygame.display.set_caption("Agar.io")
cell_list = list()
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("Ubuntu-B.ttf",20)
    big_font = pygame.font.Font("Ubuntu-B.ttf",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)

def drawText(message,pos,color=(255,255,255)):
        surface.blit(font.render(message,1,color),pos)

def getDistance(pos1,pos2):
    px,py = pos1
    p2x,p2y = pos2
    diffX = math.fabs(px-p2x)
    diffY = math.fabs(py-p2y)

    return ((diffX**2)+(diffY**2))**(0.5)

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = screen_width
        self.height = screen_height
        self.zoom = 1.0
   
    def centre(self,blobOrPos):
        if(isinstance(blobOrPos,Player)):
            p = blobOrPos
            self.x = (p.startX-p.x)-p.startX+250
            self.y = (p.startY-p.y)-p.startY+250
        elif(type(blobOrPos) == tuple):
            self.x,self.y = blobOrPos

class Player:
    def __init__(self,surface,name = ""):
        self.startX = self.x = random.randint(100,400)
        self.startY = self.y = random.randint(100,400)
        self.mass = 20
        self.surface = surface
        self.color = colors_players[random.randint(0,len(colors_players)-1)]
        self.name = name
    
    def update(self):
        self.move()
        self.collisionDetection()

    def collisionDetection(self):
        for cell in cell_list:
            if(getDistance((cell.x,cell.y),(self.x,self.y)) <= self.mass):
                self.mass+=2
                cell_list.remove(cell)

    def move(self):
        dX,dY = pygame.mouse.get_pos()
        rotation = math.atan2(dY-250,dX-250)*180/math.pi
        speed = 2
        vx = speed * (90-math.fabs(rotation))/90
        vy = 0
        if(rotation < 0):
            vy = -speed + math.fabs(vx)
        else:
            vy = speed - math.fabs(vx)
        self.x += vx
        self.y += vy
        
    def draw(self,cam):
        pygame.draw.circle(self.surface,self.color,(int(self.x+cam.x),int(self.y+cam.y)),int(self.mass))
        pygame.draw.circle(self.surface,(self.color[0]-int(self.color[0]/3),int(self.color[1]-self.color[1]/3),int(self.color[2]-self.color[2]/3)),(int(self.x+cam.x),int(self.y+cam.y)),int(self.mass+3))
        if(len(self.name) > 0):
            fw, fh = font.size(self.name)
            drawText(self.name, (self.x+cam.x-int(fw/2),self.y+cam.y-int(fh/2)),(50,50,50))

class Cell:
    def __init__(self,surface):
        self.x = random.randint(20,480)
        self.y = random.randint(20,480)
        self.mass = 7
        self.surface = surface
        self.color = colors_cells[random.randint(0,len(colors_cells)-1)]
        
    def draw(self,cam):
        pygame.draw.circle(self.surface,self.color,(int(self.x+cam.x),int(self.y+cam.y)),self.mass)

def spawn_cells():
    for i in range(0,120):
        cell = Cell(surface)
        cell_list.append(cell)
        
def draw_grid():
    for i in range(0,screen_width,20):
        pygame.draw.line(surface,(234,242,246),(0+camera.x,i+camera.y),(screen_width+camera.x,i+camera.y))
        pygame.draw.line(surface,(234,242,246),(i+camera.x,0+camera.y),(i+camera.x,screen_height+camera.y))

camera = Camera()
blob = Player(surface,"Viliami")
spawn_cells()

def draw_HUD():
    w,h = font.size("Score: "+str(blob.mass)+" ")
    surface.blit(pygame.transform.scale(t_surface,(w,h)),(8,screen_height-30))
    surface.blit(t_lb_surface,(screen_width-160,15))
    drawText("Score: " + str(blob.mass),(10,screen_height-30))
    surface.blit(big_font.render("Leaderboard",0,(255,255,255)),(screen_width-157,20))
    drawText("1. G #1",(screen_width-157,20+25))
    drawText("2. G #2",(screen_width-157,20+25*2))
    drawText("3. ISIS",(screen_width-157,20+25*3))
    drawText("4. ur mom",(screen_width-157,20+25*4))
    drawText("5. w = pro team",(screen_width-157,20+25*5))
    drawText("6. jumbo",(screen_width-157,20+25*6))
    drawText("7. [voz]plz team",(screen_width-157,20+25*7))
    drawText("8. G #3",(screen_width-157,20+25*8))
    drawText("9. doge",(screen_width-157,20+25*9))
    drawText("10. G #4",(screen_width-157,20+25*10))

while(True):
    clock.tick(60)
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
        if(e.type == pygame.QUIT):
            pygame.quit()
    blob.update()

    camera.centre(blob)
    surface.fill((242,251,255))
    #surface.fill((0,0,0))
    draw_grid()
    for c in cell_list:
        c.draw(camera)
    blob.draw(camera)
    draw_HUD()
    pygame.display.flip()
