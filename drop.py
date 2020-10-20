import pygame
import sys
pygame.init()
size = (450, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pix Drop")
icon = pygame.transform.scale(pygame.image.load("pix.png"), (32, 32))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
fps = 60
click = False
def menu(): 
    pix_Img = pygame.image.load("pix.png")
    # pix_Img = pygame.transform.scale(pix_Img, (pix_Img.get_width()//2, pix_Img.get_height()//2))
    start = pygame.image.load("start_btn.png")
    x = 0
    dx = 1
    running = True
    while running:
        screen.fill((255,255,255))
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
    dx = 5
    dy = 20
    plat_Img = pygame.image.load("platform_long.png")
    # plat_Img = pygame.transform.scale(plat_Img, (plat_Img.get_width(), plat_Img.get_height()))
    plat_X = 0
    plat_Y = 100
    running = True
    collide = False
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        save_y = pix_Y
        pix_Y += dy
        if pix_Y + pix_Img.get_height() > plat_Y + plat_Img.get_height():
            pix_Y = save_y
            dy = 0
            collide = True
        if collide:
            pix_X += dx

        plat_X += dx

        if plat_X <= 0:
            dx *= -1
        elif plat_X >= size[0]-plat_Img.get_width():
            dx *= -1
        screen.blit(pix_Img, (pix_X, pix_Y))
        screen.blit(plat_Img, (plat_X, plat_Y))
        pygame.display.flip()
        clock.tick(fps)
        
menu()
pygame.quit()