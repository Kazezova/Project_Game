import sys
import pygame
from random import randint as rand

pygame.init()
#game branding
pygame.display.set_caption("Pix Drop")
icon = pygame.transform.scale(pygame.image.load("pix.png"), (32, 32))
pygame.display.set_icon(icon)

#frame settings
size = (450, 750)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

#images
platform_images = ["platform_long.png", "platform_short.png"]
enemy_images = ["kill_long.png", "kill_short.png"]
py_platform = [(pygame.image.load(i), i) for i in platform_images]
py_enemy = [(pygame.image.load(i), i) for i in enemy_images]
back_img = pygame.image.load("angryimg.png")
cloud_img = pygame.image.load("cloud.png")
opp = pygame.image.load("download.png")
cont = pygame.image.load("continue.png")

#platfroms
data = [
    [0, 100,  py_platform[rand(0, len(py_platform)-1)]], 
    [rand(0,100), 200, py_platform[rand(0, len(py_platform)-1)]], 
    [rand(0,100), 300, py_enemy[rand(0, len(py_enemy)-1)]], 
    [rand(0,100), 400, py_enemy[rand(0, len(py_enemy)-1)]],
    [rand(0,100), 500, py_enemy[rand(0, len(py_enemy)-1)]]
]

#cloud 
cloud_x = 400
cloud_dx = -1

class Pix:

    dy = 7

    def __init__(self, x, y, image):
        self.image = image
        self.height = image.get_height()
        self.width = image.get_width()
        self.x = x
        self.y = y

    def draw(self, size=None):
        if size == None:
            screen.blit(self.image, (self.x, self.y))
        else:
            screen.blit(pygame.transform.scale(self.image, size), (self.x, self.y))

    def fall(self):
        Pix.dy = 7
        self.y += Pix.dy

    def collide(self, smth):
        if self.y + self.height >= smth.y and (self.x+self.width>smth.x and self.x<smth.x+smth.width):
            Pix.dy = 0
            self.y = smth.y - self.height
            self.x += smth.dx
            return True
        return False


class Platform:
    def __init__(self, x, y, image, picname):
        self.image = image
        self.picname = picname
        self.x = x
        self.y = y
        self.height = image.get_height()
        self.width = image.get_width()
        self.dx = 3

    def move(self):
        self.x += self.dx
        if self.x <= 0:
            self.dx *= -1
        elif self.x>= size[0]-self.width:
            self.dx *= -1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def __del__(self):
        pass

class Enemy(Platform):
    def __init__(self, x, y, image, picname):
        super().__init__(x, y, image, picname)

platforms = [Platform(data[i][0], data[i][1], data[i][2][0], data[i][2][1]) for i in range(2)]
enemys = [Enemy(data[i][0], data[i][1], data[i][2][0], data[i][2][1]) for i in range(2,5)]

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

click = False        
def menu(): 
    pix_Img = pygame.image.load("pix.png")
    pix_Img = pygame.transform.scale(pix_Img, (pix_Img.get_width()//2, pix_Img.get_height()//2))
    start = pygame.image.load("play_btn.png")
    x = 0
    dx = 1
    running = True

    while running:
        background()
        mx, my = pygame.mouse.get_pos()
        btn = pygame.Rect(size[0]//2-start.get_width()//2 + x, 
                            size[1] //3 + pix_Img.get_height(), 
                            start.get_width(), 
                            start.get_height()
                            )
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        if btn.collidepoint((mx, my)):
            if click:
                game(pix_Img, 0)
                running = False

        x += dx
        if x <= -25:
            dx *= -1
        elif x >= 25:
            dx *= -1

        screen.blit(pix_Img, (size[0]//2-pix_Img.get_width()//2 + x , size[1]//3))
        screen.blit(start, (size[0]//2-start.get_width()//2 + x, size[1]//3 + pix_Img.get_height()))
        pygame.display.flip()
        clock.tick(fps)

def game(pix_Img, score):
    global platforms, enemys
    pix_X = 70
    pix_Y = -20
    my_pix = Pix(pix_X, pix_Y, pix_Img)
    running = True
    fall = False
    while running:
        background()
        col = my_pix.collide(platforms[0])
        if col==False:
            my_pix.draw((my_pix.width, my_pix.height+20))
            my_pix.fall()
        elif col==True and fall==True:
            if 'long' in enemys[0].picname:
                image = py_platform[0]
            elif 'short' in enemys[0].picname:
                image = py_platform[1]
            platforms.append(Platform(enemys[0].x, enemys[0].y, image[0], image[1]))
            del enemys[0]
            new = data[rand(2,4)]
            enemys.append(Enemy(new[0], enemys[-1].y+100, new[2][0], new[2][1]))
            my_pix.draw()
            fall = False
        else:
            my_pix.draw()

        if my_pix.y > platforms[0].y + platforms[0].height and col == False:
            continue_game(pix_Img, 20)
            running = False

        for i in range(len(platforms)):
            platforms[i].move()
            platforms[i].draw()
        for i in range(len(enemys)):
            enemys[i].move()
            enemys[i].draw()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    menu()
                # if event.key == pygame.K_SPACE:
                #     my_pix.fall()
                #     del platforms[0]
                #     platforms.append(Platform.generator(enemys[0]))
                #     del enemys[0]
                #     enemys.append(Enemy.generator())
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    fall = True
                    del platforms[0]
                    my_pix.fall()

        pygame.display.flip()
        clock.tick(fps)

def continue_game(pix, score):
    global platforms, enemys
    running = True
    while running:
        background()
        for i in range(len(platforms)):
            platforms[i].move()
            platforms[i].draw()
        for i in range(len(enemys)):
            enemys[i].move()
            enemys[i].draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game(pix, score)
        s = pygame.Surface((size[0],size[1]), pygame.SRCALPHA)   
        s.fill((0,0,0,32)) 
        screen.blit(s, (0,0))
        screen.blit(cont, (size[0]//2-cont.get_width()//2, size[1]//2-cont.get_height()//2))
        pygame.display.flip()
        clock.tick(fps)

menu()
pygame.quit()