import pygame
import sqlite3
from random import randint as rnd

pygame.init()
# gamebranding
icon = pygame.transform.scale(pygame.image.load("pix32.png"), (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption("Pix Drop")
myfont = pygame.font.SysFont('Comic Sans MS', 40)

# database connect
conn = sqlite3.connect('dropDB.sqlite')
cur = conn.cursor()

# fonts
font1 = pygame.font.Font('Jesus_Lives.ttf', 60)
font2 = pygame.font.Font('Jesus_Heals.ttf', 60)
font2bs = pygame.font.Font('Jesus_Heals.ttf', 32)

# settings
size = (450, 750)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60

x, y = 200, 100
dx, dy = 0, 0
plat_x, plat_y = 150, 300
gravity = 1
dx = 2

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE2 = (47, 109, 246)
YELLOW = (249, 229, 106)


# LOAD IMAGES
# background
back_img = pygame.image.load("angryimg.png")
cloud_img = pygame.image.load("download.png")
# pix
pix_img = pygame.image.load("pix32.png")
pix_img = pygame.transform.scale(pix_img, (32, 32))
pix_dead_img = pygame.image.load("pix_kill32.png")
# platforms
plats_imgs = ["platform_long.png", "platform_short.png"]
enemy_imgs = ["kill_long.png", "kill_short.png"]
plat_img_list = [pygame.image.load(i) for i in plats_imgs]
enemy_img_list = [pygame.image.load(i) for i in enemy_imgs]
# buttons
start_btn = pygame.image.load("play_btn.png")
bomb_img = pygame.image.load("bomb.png")
best_score_img = pygame.image.load("best_score.png")
# bonuses


# platforms data
dist = 120
q_plat = len(plat_img_list)


class Pix():
    def __init__(self, x, y, image, dx, dy):
        self.x = x
        self.y = y
        self.img = image
        self.width = image.get_width()
        self.hight = image.get_height()
        self.x_right = self.x + image.get_width()
        self.y_bot = self.y + image.get_height()
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.x_right += self.dx
        self.y += self.dy
        self.y_bot += self.dy

    def draw(self, camera_y):
        screen.blit(self.img, (self.x, self.y-camera_y))

    def collide(self, other):
        half_pix_x = self.width//2
        if self.x + half_pix_x <= other.x_right and self.x_right - half_pix_x >= other.x and self.y_bot >= other.y and self.y <= other.y_bot:
            return True
        return False

    def col_left(self, other):
        half_pix_x = self.width//2
        if self.x+half_pix_x <= other.x and self.x_right >= other.x and self.y_bot >= other.y and self.y <= other.y_bot:
            return True
        return False

    def col_right(self, other):
        half_pix_x = self.width//2
        if self.x_right-half_pix_x >= other.x_right and self.x <= other.x_right and self.y_bot >= other.y and self.y <= other.y_bot:
            return True
        return False

    def isalive(self, other):
        # half_pix_x = self.width//2
        if self.y_bot - 2 <= other.y:
            return True
        return False


class Button():
    def __init__(self, x, y, image, dx, dy):
        self.x = x
        self.y = y
        self.img = image
        self.width = image.get_width()
        self.hight = image.get_height()
        self.x_right = self.x + image.get_width()
        self.y_bot = self.y + image.get_height()
        self.dx = dx
        self.dy = dy

    def isclick(self, click):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x > self.x and mouse_x < self.x_right) and (mouse_y > self.y and mouse_y < self.y_bot) and click:
            return True
        return False

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, left_margin, right_margin):
        self.x += self.dx
        self.x_right += self.dx
        if self.x > right_margin or self.x < left_margin:
            self.dx *= -1


class Platform():
    def __init__(self, x, y, image, dx, dy, isenemy, img_num):
        self.x = x
        self.y = y
        self.img = image
        self.width = image.get_width()
        self.hight = image.get_height()
        self.x_right = self.x + image.get_width()
        self.y_bot = self.y + image.get_height()
        self.dx = dx
        self.dy = dy
        self.isenemy = isenemy
        self.img_num = img_num

    def draw(self, camera_y):
        screen.blit(self.img, (self.x, self.y-camera_y))

    def move(self):
        self.x += self.dx
        self.x_right += self.dx
        self.y += self.dy
        self.y_bot += self.dy
        if self.x < 0 or self.x_right > 450:
            self.dx *= -1


cloud_dist = 70
cloud_list = [[rnd(0, 400), cloud_dist*(i+1) + rnd(0, 20), rnd(1, 3)]
              for i in range(8)]


def background():
    global cloud_list
    screen.blit(back_img, (0, 0))
    for i in range(len(cloud_list)):
        screen.blit(cloud_img, (cloud_list[i][0], cloud_list[i][1]))
        cloud_list[i][0] -= cloud_list[i][2]
        if cloud_list[i][0] < -50:
            cloud_list[i][0] = 500


def cam_shake(cam_shake_cnt, camera_y):
    if cam_shake_cnt <= 15:
        camera_y += rnd(-7, 7)
    return camera_y


def timer_draw(timer_cnt):
    pygame.draw.rect(screen, BLUE2, (172, 127, 106, 16))
    pygame.draw.rect(screen, WHITE, (173, 128, 104, 14))
    pygame.draw.rect(screen, BLUE2, (175, 130, 100, 10))
    pygame.draw.rect(screen, YELLOW, (176, 131, timer_cnt//3, 8))


def menu():
    pix = Pix(218, 250, pix_img, 0, 3)
    play_btn = Button(161, 311, start_btn, 1, 0)
    best_score = Button(175, 212, best_score_img, 1, 0)
    run = True
    collide = False
    best_score_x = 212
    best_score_dx = 1
    user_stars = cur.execute('SELECT stars FROM User').fetchone()[0]
    user_best_score = cur.execute('SELECT best_score FROM User').fetchone()[0]
    while run:
        background()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        collide = pix.collide(play_btn)

        if not collide:
            pix.dx = 0
            pix.dy = 3
        else:
            pix.dx = play_btn.dx
            pix.y = play_btn.y - pix.hight
            pix.dy = 0

        pix.move()
        play_btn.move(140, 180)
        play_btn.draw()
        best_score.move(154, 194)
        best_score.draw()

        best_score_x += best_score_dx
        if best_score_x < 191 or best_score_x > 231:
            best_score_dx *= -1
        screen.blit(font2bs.render(
            f"{str(user_best_score).zfill(2)}", False, BLUE2), (best_score_x, 219))
        pix.draw(0)
        screen.blit(myfont.render(
            f"{pix.x_right, pix.y, collide}", False, RED), (50, 50))

        if play_btn.isclick(click):
            game(pix_img, 0)
            run = False

        pygame.display.flip()
        clock.tick(FPS)


def game(pix_img, score):
    pix = Pix(130, 100, pix_img, 0, 5)
    run = True
    bomb_btn = Button(50, 650, bomb_img, 0, 0)

    # dead
    rotate_left = False
    rotate_right = False
    spin = 0

    # plats list creation
    plats = []
    plat_i = 0
    plat_1_save = False
    first_plat = Platform(0, 200, plat_img_list[0], 3, 0, False, 0)
    plats.append(first_plat)

    # timer cnt
    timer_cnt = 294
    istimer = False
    # camera settings
    camera_fall = False
    camera_count = 0
    camera_y = 0
    cam_shake_cnt = 0

    # click_settings
    clickable = False
    click_interval = 40
    click_count = 0
    plat_save_i = 0

    while run:
        background()

        isalive = pix.isalive(plats[0])
        col_right = pix.col_right(plats[0])
        col_left = pix.col_left(plats[0])

        if col_left or col_right:
            isalive = False

        collide = False

        # click mechanics
        click = False
        click_count += 1
        if click_count > click_interval:
            clickable = True

        # plats creation
        while len(plats) != 5:
            plat_i += 1
            # next platform image(npi)
            npi = rnd(0, q_plat-1)
            next_plat = Platform(rnd(0, 250), 200 + plat_i *
                                 dist-9, enemy_img_list[npi], rnd(2, 4), 0, True, npi)
            plats.append(next_plat)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if clickable:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                        clickable = False
                        click_count = 0
                        camera_fall = True
                        camera_count -= 40

        # bomb mechanics
        if isalive:
            if bomb_btn.isclick(click):
                plats.pop(1)
                camera_fall = True
                plat_save_i = 0
                plat_1_save = True
                camera_fall = False
                camera_count = 0
                score -= 1
        if plat_1_save:
            plat_save_i += 1
            if plat_save_i <= 40:
                for j in range(1, len(plats)):
                    plats[j].y -= 3
            else:
                plat_i -= 1
                plat_1_save = False

        if click and isalive and not bomb_btn.isclick(click):
            plats.pop(0)

        # collison mechanics
        collide = pix.collide(plats[0])
        if not collide:
            pix.dx = 0
            pix.dy = 5
            pix.img = pygame.transform.scale(pix.img, (32, 38))
        elif isalive:
            pix.dx = plats[0].dx
            pix.y = plats[0].y - pix.hight
            pix.dy = 0
            pix.img = pygame.transform.scale(pix_img, (32, 32))
            deletable = True
            istimer = True
            # next plat ally
            if plats[1].isenemy == True:
                plats[1].isenemy = False
                plats[1].img = plat_img_list[plats[1].img_num]
                plats[1].y += 9
                timer_cnt = 294
                if plat_i != len(plats)-1:
                    score += 1

        # camera fall mechanics
        if camera_fall:
            camera_y += 3
            camera_count += 1
            if camera_count == 0:
                camera_fall = False

        # dead mechanics
        if col_left:
            cam_shake_cnt += 1
            camera_y = cam_shake(cam_shake_cnt, camera_y)
            rotate_left = True
        if col_right:
            cam_shake_cnt += 1
            camera_y = cam_shake(cam_shake_cnt, camera_y)
            rotate_right = True

        if not isalive:
            click_count = 0
            for i in range(1, len(plats)):
                collide = pix.collide(plats[i])
                col_right = pix.col_right(plats[i])
                col_left = pix.col_left(plats[i])
                if col_left:
                    cam_shake_cnt += 1
                    camera_y = cam_shake(cam_shake_cnt, camera_y)
                    rotate_left = True
                if col_right:
                    cam_shake_cnt += 1
                    camera_y = cam_shake(cam_shake_cnt, camera_y)
                    rotate_right = True
                if collide and not(rotate_right or rotate_left):
                    pix.img = pix_dead_img
                    pix.img = pygame.transform.scale(pix.img, (32, 25))
                    pix.dx = plats[i].dx
                    pix.y = plats[i].y - pix.hight+7
                    pix.dy = 0
                    cam_shake_cnt += 1
                    camera_y = cam_shake(cam_shake_cnt, camera_y)

        # rotate if pix touches edge
        if rotate_left:
            spin += 3
            pix.dx = -3
            pix.img = pygame.transform.rotate(pix_dead_img, spin)

        if rotate_right:
            spin -= 3
            pix.dx = 3
            pix.img = pygame.transform.rotate(pix_dead_img, spin)

        # plats drawing
        for i in range(len(plats)):
            plats[i].move()
            plats[i].draw(camera_y)

        # score drawing
        if score < 100:
            screen.blit(font1.render(
                f"{str(score).zfill(2)}", False, BLUE), (200, 50))
            screen.blit(font2.render(
                f"{str(score).zfill(2)}", False, WHITE), (200, 52))

        # timer mechanics
        timer_draw(timer_cnt)
        if istimer:
            timer_cnt -= 1
            if timer_cnt <= 0:
                timer_cnt = 0
                if deletable:
                    plats.pop(0)
                    camera_count -= 40
                    camera_fall = True
                    deletable = False

        pix.move()
        pix.draw(camera_y)
        bomb_btn.draw()
        screen.blit(myfont.render(
            f"{plat_save_i}", False, RED), (50, 50))
        pygame.display.flip()
        clock.tick(FPS)


menu()

pygame.quit()
