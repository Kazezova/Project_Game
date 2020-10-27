import pygame

pygame.init()
#set game's branding
icon = pygame.transform.scale(pygame.image.load("pix.png"), (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption("Pix Drop")
myfont = pygame.font.SysFont('Comic Sans MS', 40)

size = (450, 750)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60

x, y = 200, 100
dx, dy = 0, 0
plat_x, plat_y = 150, 300
gravity = 1
dx = 2
margin = 20

#colors
WHITE = (255,255,255)
init_pix_x = 70
init_pix_x = -20

#load images
pix_img = pygame.image.load("pix.png")
plat_img = pygame.image.load("platform_long.png")
pix_img = pygame.transform.scale(pix_img, (50, 50))
pix_height = pix_img.get_height()
plat_height = plat_img.get_height()
plat_width = plat_img.get_width()


class Pix:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.height = image.get_height()
        self.width = image.get_width()

    def fall(self):
        self.y -= gravity

    def collide(self,other):
        if (self.y+self.height > other.y) and (self.x+self.width > other.x and self.x < other.x+other.width):
            dy = 0
            self.x +=other.dx
            self.y = other.y - self.height
            return True
        return False

class Platform:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.height = image.get_height()
        self.width = image.get_width()
        
    def move(self):


def game():
    run = True
    pix = Pix(50,50,pix_img)
    plat = (200,200,plat_img)
    dy = 0
    while run:
        screen.fill(WHITE)
        #gravity
        dy += gravity
        if dy > 5:
            dy = 5
        pix.y += dy

        if plat.x>(450-plat_width-margin) and dx>0:
            dx = -2
        elif plat_x<margin and dx<0:
            dx = 2
        plat_x += dx

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        screen.blit(pix.image, (pix.x, pix.y))
        screen.blit(plat.image, (plat.x, plat.y))
        screen.blit(myfont.render(
             f"{plat_y}, {collide},{plat_img.get_height()}", False, (255, 0, 0)), (50, 50))
        pygame.display.flip()
        clock.tick(FPS)
game()
pygame.quit()
