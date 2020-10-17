import pygame
pygame.init()
size = (450, 750)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 20

pygame.display.set_caption("Pix Drop")
icon = pygame.image.load("pix.png")
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

pix_size = 50
pix_Img = pygame.image.load("pix.png")
pix_Img = pygame.transform.scale(pix_Img, (pix_size, pix_size))
pix_X = 70
pix_Y = -20

dx = 10
dy = 20

plat_Img = pygame.image.load("platform_long.png")
plat_Img = pygame.transform.scale(plat_Img, (plat_Img.get_width(), plat_Img.get_height()))
plat_X = 0
plat_Y = 100

def pix(x,y):
    screen.blit(pix_Img, (x, y))

def plat(x,y):
    screen.blit(plat_Img, (x, y))

running = True
collide = False
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    save_y = pix_Y
    pix_Y += dy

    if pix_Y == plat_Y:
        pix_Y = save_y
        dy = 0
        collide = True
    if collide:
        pix_X += dx
    
    plat_X += dx

    if plat_X <= 0:
        plat_X = 0
        if dx<0:
            dx *= -1
    elif plat_X >= size[0]-plat_Img.get_width()//2:
        plat_X = size[0]-plat_Img.get_width()//2
        dx *= -1
    # screen.blit(pix_Img, (size[0]/2-pix_size/2, 200))
    pix(pix_X, pix_Y)
    plat(plat_X, plat_Y)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()