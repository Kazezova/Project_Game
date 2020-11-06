import pygame

pygame.init()
size = (450, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pix Drop")
icon = pygame.image.load("pix.png")
pygame.display.set_icon(pygame.transform.scale(icon, (32, 32)))
clock = pygame.time.Clock()
fps = 40

class MenuScene:
    def __init__(self, pixel):
        self.pixel = pixel
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('YES')
                scene = scenes['Main']
    def draw(self):
        screen.fill((255,255,255))
        screen.blit(self.pixel, (size[0]//2-self.pixel.get_width()//2, 200))
        pygame.display.flip()
        clock.tick(fps)

# dx = 5
# dy = 10
# plat_Img = pygame.image.load("platform_long.png")
# plat_Img = pygame.transform.scale(plat_Img, (plat_Img.get_width(), plat_Img.get_height()))
# plat_X = 0
# plat_Y = 100
# collide = False
class MainScene:
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            print('YES')
            if event.key == pygame.K_ESC:
                scene = scenes['Menu']
    def draw(self):
        screen.fill((255,255,255))
        pygame.display.flip()
        clock.tick(fps)
    # def __init__(self, pixel, pix_x, pix_y):
    #     self.pixel = pixel
    #     self.pix_x = pix_x
    #     self.pix_y = pix_y
    #     self.platform = plat_Img
    #     self.x = plat_X
    #     self.y = plat_Y
    #     self.dx = dx
    #     self.dy = dy
    
    # def draw(self):
    #     save_y = self.pix_y
    #     self.pix_y += self.dy

    #     if self.pix_y == plat_Y:
    #         self.pix_y = save_y
    #         self.dy = 0
    #         collide = True
    #     if collide:
    #         self.pix_y += self.dx
        
    #     self.x += self.dx

    #     if self.x <= 0:
    #         self.x = 0
    #         if self.dx<0:
    #             self.dx *= -1
    #     elif self.x >= size[0]-self.platform.get_width()//2:
    #         self.x = size[0]-self.platform.get_width()//2
    #         self.dx *= -1
    #     screen.blit(self.pixel, (self.pix_x, self.pix_y))
    #     screen.blit(self.platform, (self.x, self.y))
    #     pygame.display.flip()
    #     clock.tick(fps)

pix_size = 50
pix_Img = pygame.transform.scale(pygame.image.load("pix.png"), (pix_size, pix_size))
pix_X = 70
pix_Y = -20

scenes = {'Menu': MenuScene(pix_Img),
          'Main': MainScene()}
scene = scenes['Menu']

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.handle_event(event)
        scene.draw()
pygame.quit()