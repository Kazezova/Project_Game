import pygame
import sys
pygame.init()
size = (450, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pix Drop")
icon = pygame.transform.scale(pygame.image.load("pix.png"), (32, 32))
pygame.display.set_icon(icon)
back_img = pygame.image.load("angryimg.png")
cloud_img = pygame.image.load("cloud.png")
opp = pygame.image.load("download.png")
cloud_x = 400
cloud_dx = -1
clock = pygame.time.Clock()
fps = 60
click = False

class Pix:
    dy = 7
    def __init__(self, x, y, image):
        self.image = image
        self.height = image.get_height()
        self.width = image.get_width()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
    def draw(self, size=None):
        if size == None:
            screen.blit(self.image, (self.x, self.y))
        else:
            screen.blit(pygame.transform.scale(self.image, size), (self.x, self.y))
    def fall(self):
        Pix.dy = 7
        self.y += Pix.dy
    def collide(self, smth):
        if self.y + self.height >= smth.y and (self.x+self.width>smth.x and self.x+self.width<smth.x+smth.width):
            Pix.dy = 0
            self.y = smth.y - self.height
            self.x += smth.dx
            return True
        return False

class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.height = image.get_height()
        self.width = image.get_width()
        self.dx = 3
        self.rect = self.image.get_rect()
        
    def move(self):
        self.x += self.dx
        if self.x <= 0:
            self.dx *= -1
        elif self.x>= size[0]-self.width:
            self.dx *= -1
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def generator(ene):
        new = Platform(ene.x, ene.y, pygame.image.load("platform_short.png"))
        return new  
    def __del__(self):
        pass

class Enemy(Platform):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
    def generator():
        new = Enemy(20, 600, pygame.image.load("platform1_kill.png"))
        return new  

def background():
    global cloud_x
    screen.blit(back_img, (0,0))
    if cloud_x + opp.get_width() + 400 < 0:
        cloud_x = 600
    cloud_x += -2
    screen.blit(opp, (cloud_x+200, 100))
    screen.blit(opp, (cloud_x+50, 50))
    screen.blit(opp, (cloud_x, 150))
    screen.blit(opp, (cloud_x-150, 300))
        
def menu(): 
    pix_Img = pygame.image.load("pix.png")
    pix_Img = pygame.transform.scale(pix_Img, (pix_Img.get_width()//2, pix_Img.get_height()//2))
    start = pygame.image.load("start_btn.png")
    x = 0
    dx = 1
    running = True
    while running:
        background()
        x += dx
        if x <= -25:
            dx *= -1
        elif x >= 25:
            dx *= -1
        mx, my = pygame.mouse.get_pos() 
        btn = pygame.Rect(size[0]//2-start.get_width()//2 + x, size[1]//3 + pix_Img.get_height(), start.get_width(), start.get_height())
        if btn.collidepoint((mx, my)):
            if click:
                game(pix_Img)
                running = False
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        screen.blit(pix_Img, (size[0]//2-pix_Img.get_width()//2 + x , size[1]//3))
        screen.blit(start, (size[0]//2-start.get_width()//2 + x, size[1]//3 + pix_Img.get_height()))
        pygame.display.flip()
        clock.tick(fps)

def game(pix_Img):
    pix_X = 70
    pix_Y = -20
    my_pix = Pix(pix_X, pix_Y, pix_Img)
    
    platforms = []
    enemys = []
    plat_Img = pygame.image.load("platform_long.png")
    plat_X = 0
    plat_Y = 100
    data = [[0, 100, "platform_long.png"], [0, 200, "platform_short.png"], [0, 300, "platform1_kill.png"], 
    [0, 400, "platform2_kill.png"],
    [0, 500, "platform1_kill.png"]]
    for i in range(2):
        platforms.append(Platform(data[i][0], data[i][1], pygame.image.load(data[i][2])))
    for i in range(2, 5):
        enemys.append(Enemy(data[i][0], data[i][1], pygame.image.load(data[i][2])))
    running = True
    collide = False
    while running:
        background()
        my_pix.fall()
        col = my_pix.collide(platforms[0])
        if my_pix.y > platforms[0].y + platforms[0].height and col == False:
            print('Game OVER!')
        for i in range(len(platforms)):
            platforms[i].move()
        for i in range(len(enemys)):
            enemys[i].move()
        if col==False:
            my_pix.draw((my_pix.width, my_pix.height+20))
        else:
            my_pix.draw()
        for i in range(len(platforms)):
            platforms[i].draw()
        for i in range(len(enemys)):
            enemys[i].draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    menu()
                if event.key == pygame.K_SPACE:
                    my_pix.fall()
                    del platforms[0]
                    platforms.append(Platform.generator(enemys[0]))
                    del enemys[0]
                    platforms.append(Enemy.generator())
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    my_pix.fall()
                    del platforms[0]
                    platforms.append(Platform.generator(enemys[0]))
                    del enemys[0]
                    enemys.append(Enemy.generator())

        pygame.display.flip()
        clock.tick(fps)    
menu()
pygame.quit()