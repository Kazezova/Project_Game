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
gravity = 0.5
run = True
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


class pix:
    def __init__(self, x, y, image, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = image

while run:
    screen.fill(WHITE)
    #gravity
    prev_x, prev_y = x, y
    dy += gravity
    if dy > 5:
        dy = 5
    y += dy
    
    if plat_x>(450-plat_width-margin) and dx>0:
        dx = -2
    elif plat_x<margin and dx<0:
        dx = 2
    plat_x += dx

    collide = False
    if plat_y < (y+pix_height) and (y+pix_height) < (plat_y+plat_img.get_height()):
        collide = True
    if collide:
        y = plat_y-pix_height
        x += dx

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    screen.blit(pix_img, (x, y))
    screen.blit(plat_img, (plat_x, plat_y))
    # screen.blit(myfont.render(
    #     f"{plat_y}, {prev_y}, {collide},{plat_img.get_height()}",
    #     False, (255, 0, 0)), (50, 50))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
