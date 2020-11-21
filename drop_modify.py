import sys
import pygame
from random import randint as rand
import sqlite3

conn = sqlite3.connect('dropDB.sqlite')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
if cur.execute('SELECT id FROM User') == None:
    cur.execute(
        'INSERT OR IGNORE INTO User (character_id, stars, best_score) VALUES (1,0,0)')
    print('he')

all_characters = [dict(row) for row in cur.execute(
    'SELECT * FROM Character').fetchall()]

character_id = cur.execute('SELECT character_id FROM User').fetchone()[0]

user_stars = cur.execute('SELECT stars FROM User').fetchone()[0]
user_best_score = cur.execute('SELECT best_score FROM User').fetchone()[0]

pygame.init()
# game branding
pygame.display.set_caption("Pix Drop")
icon = pygame.transform.scale(pygame.image.load("pix.png"), (32, 32))
pygame.display.set_icon(icon)
font = pygame.font.Font('Jesus_Heals.ttf', 60)
bord = pygame.font.Font('Jesus_Lives.ttf', 60)
star_font = pygame.font.Font('Jesus_Heals.ttf', 28)
best_score_font = pygame.font.Font('Jesus_Heals.ttf', 32)
# frame settings
size = (450, 750)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
cloud_x = 400
cloud_dx = -1
camera_y = 0

# images
back_img = pygame.image.load("angryimg.png")
cloud_img = pygame.image.load("cloud.png")
opp = pygame.image.load("download.png")
cont = pygame.image.load("cont.png")
cont_btn_img = pygame.image.load("btn100.png")
not_cont_img = pygame.image.load("btn_cancel_1.png")
restart_btn_img = pygame.image.load("restart_btn.png")
best_score_img = pygame.image.load("best_score.png")
star = pygame.image.load("star32.png")
leaf = pygame.image.load("leaf32.png")
mushroom = pygame.image.load("mushroom32.png")
carrot = pygame.image.load("carrot32.png")
home = pygame.image.load("home.png")
bomb_img = pygame.image.load("bomb.png")

ball_green = pygame.image.load("ball_green.png")
ball_pink = pygame.image.load("ball_pink.png")
ball_violet = pygame.image.load("ball_violet.png")
ball_yellow = pygame.image.load("ball_yellow.png")
trick = {"star": star, "leaf": leaf, "mushroom": mushroom, "carrot": carrot,
         "green": pygame.transform.scale(ball_green, (24, 24)), "pink": pygame.transform.scale(ball_pink, (24, 24)),
         "violet": pygame.transform.scale(ball_violet, (24, 24)), "yellow": pygame.transform.scale(ball_yellow, (24, 24))}

bonus_platform = pygame.image.load("platform_very_long.png")
bonus_kill = pygame.image.load("platform_very_long_kill.png")
bonus_enemy = pygame.image.load("kill_long.png")
bonus_enemy = pygame.transform.scale(
    bonus_enemy, (size[0], bonus_enemy.get_height()))
star_rainbow = pygame.image.load("star_rainbow.png")

platform_images = ["platform_long.png", "platform_short.png"]
enemy_images = ["kill_long.png", "kill_short.png"]
py_platform = [(pygame.image.load(i), i) for i in platform_images]
py_enemy = [(pygame.image.load(i), i) for i in enemy_images]
# dead_pix = pygame.image.load("pix_kill100.png")
# dead_pix = pygame.transform.scale(dead_pix, (32,32))

skin_back_img = pygame.image.load("page_skins.png")
skin_btn_img = pygame.image.load("skin_btn.png")
skin_right_img = pygame.image.load("right.png")
skin_left_img = pygame.image.load("left.png")
selected = pygame.image.load("btn_selected.png")
choose = pygame.image.load("btn_select.png")
buy = pygame.image.load("btn1000.png")
cant_buy = pygame.image.load("cant_buy.png")
buy_platform = pygame.image.load("platform_unselected.png")

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
music = pygame.mixer.Sound('main.wav')
music.set_volume(0.2)
star_sound = pygame.mixer.Sound("star.wav")
trick_sound = pygame.mixer.Sound("trick.wav")
ball_sound = pygame.mixer.Sound("ball.wav")
drop_sound = pygame.mixer.Sound("del_platform.wav")
start_sound = pygame.mixer.Sound("start.wav")
fall_sound = pygame.mixer.Sound("fall.wav")
dead_sound = pygame.mixer.Sound("dead.wav")
restart_sound = pygame.mixer.Sound("restart.wav")
bonus_sound = pygame.mixer.Sound("bonus.wav")
bonus_star_sound = pygame.mixer.Sound("bonus_star.wav")
press_sound = pygame.mixer.Sound("press.wav")
music.play(-1)
# platfroms
itn = (0, 200)
dst = 120
data = [
    [itn[0], itn[1],  py_platform[rand(0, len(py_platform)-1)]],
    [rand(0, itn[1]), itn[1]+dst, py_platform[rand(0, len(py_platform)-1)]],
    [rand(0, itn[1]), itn[1]+dst*2, py_enemy[rand(0, len(py_enemy)-1)]],
    [rand(0, itn[1]), itn[1]+dst*3, py_enemy[rand(0, len(py_enemy)-1)]],
    [rand(0, itn[1]), itn[1]+dst*4, py_enemy[rand(0, len(py_enemy)-1)]]
]


# color
RED = (255, 0, 0)
pix_dead_img = pygame.image.load("pix_kill32.png")
# cloud
cloud_x = 400
cloud_dx = -1


class Pix:
    dy = 7
    dif = 0

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
            screen.blit(pygame.transform.scale(
                self.image, size), (self.x, self.y))

    def fall(self):
        Pix.dy = 7
        self.y += Pix.dy

    def collide(self, smth):
        if smth.special:
            if smth.x >= size[0]+smth.width or smth.x <= -smth.width:
                self.x = smth.x + Pix.dif
        if self.x + self.width//2 >= smth.x and self.x + self.width//2 <= smth.x + smth.width:
            if self.y+self.height >= smth.y and self.y <= smth.y + smth.height:
                smth.opacity = 0
                Pix.dif = self.x - smth.x
                Pix.dy = 0
                self.y = smth.y - self.height
                self.x += smth.dx
                return True
        return False

    def col_left(self, smth):
        half_pix_x = self.width//2
        if self.x+half_pix_x <= smth.x and self.x + self.width >= smth.x:
            if self.y+self.height >= smth.y and self.y <= smth.y + smth.height:
                return True
        return False

    def col_right(self, smth):
        half_pix_x = self.width//2
        if self.x + half_pix_x >= smth.x + smth.width and self.x <= smth.x + smth.width:
            if self.y+self.height >= smth.y and self.y <= smth.y + smth.height:
                return True
        return False

    def collide_enemy(self, smth):
        half_pix_x = self.width//2
        if self.x + half_pix_x <= smth.x + smth.width and self.x + half_pix_x >= smth.x:
            if self.y + self.height >= smth.y and self.y <= smth.y + smth.height:
                return True
        return False


class Platform:
    cnt = 0
    sz = 0

    def __init__(self, x, y, image, picname, dx=3, special=False, opacity=0, alpha=2, trick=None, trick_name=None, move_sharply=False):
        self.image = image
        self.picname = picname
        self.x = x
        self.y = y
        self.height = image.get_height()
        self.width = image.get_width()
        self.dx = dx
        self.special = special
        self.opacity = opacity
        self.alpha = alpha
        self.trick = trick
        self.trick_name = trick_name
        self.move_sharply = move_sharply

    def move(self):
        if self.special:
            self.x += self.dx
            if self.x > size[0]+self.width:
                self.x = - self.width
        else:
            self.x += self.dx
            if self.x <= 0:
                self.dx *= -1
            elif self.x >= size[0]-self.width+2:
                self.dx *= -1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def draw_alpha(self):
        s = pygame.Surface((self.width, self.height)).convert()
        self.opacity += self.alpha
        if self.opacity >= 254 or self.opacity <= 4:
            self.alpha *= -1
        s.blit(screen, (-self.x, -self.y))
        s.blit(self.image, (0, 0))
        s.set_alpha(self.opacity)
        screen.blit(s, (self.x, self.y))

    def draw_smth(self, smth):
        if smth != None:
            if self.opacity == 0:
                if Platform.sz < smth.get_width():
                    screen.blit(pygame.transform.scale(smth, (Platform.sz, Platform.sz)),
                                (self.x+(self.width//2)-Platform.sz//2, self.y-Platform.sz-10))
                else:
                    screen.blit(smth, (self.x+(self.width//2) -
                                       smth.get_width()//2, self.y-smth.get_height()-10))
            else:
                if Platform.sz < smth.get_width():
                    s = pygame.Surface((Platform.sz, Platform.sz)).convert()
                    s.blit(screen, (-(self.x+(self.width//2) -
                                      Platform.sz//2), -(self.y-Platform.sz-10)))
                    s.blit(pygame.transform.scale(
                        smth, (Platform.sz, Platform.sz)), (0, 0))
                    s.set_alpha(self.opacity)
                    screen.blit(s, (self.x+(self.width//2) -
                                    Platform.sz//2, self.y-Platform.sz-10))
                else:
                    s = pygame.Surface(
                        (smth.get_width(), smth.get_height())).convert()
                    s.blit(screen, (-(self.x+(self.width//2) -
                                      smth.get_width()//2), -(self.y-smth.get_height()-10)))
                    s.blit(smth, (0, 0))
                    s.set_alpha(self.opacity)
                    screen.blit(
                        s, (self.x+(self.width//2)-smth.get_width()//2, self.y-smth.get_height()-10))

            if Platform.cnt > 15 and Platform.cnt <= 30:
                Platform.sz -= 2
            else:
                Platform.sz += 2
            Platform.cnt += 1


class Enemy(Platform):
    def __init__(self, x, y, image, picname, dx=3, special=False, opacity=0, alpha=2, move_sharply=False):
        super().__init__(x, y, image, picname, dx, special,
                         opacity, alpha, None, None, move_sharply)

    def draw_smth(self, smth):
        screen.blit(smth, (self.x+(self.width//2) -
                           smth.get_width()//2, self.y-smth.get_height()-10))


def background(user_stars):
    global cloud_x
    screen.blit(back_img, (0, 0))
    if cloud_x + opp.get_width() + 400 < 0:
        cloud_x = 600
    cloud_x += -2
    screen.blit(opp, (cloud_x+200, 100))
    screen.blit(opp, (cloud_x+50, 50))
    screen.blit(opp, (cloud_x, 150))
    screen.blit(opp, (cloud_x-150, 300))
    screen.blit(pygame.transform.scale(star, (28, 28)), (10, 10))
    screen.blit(star_font.render(
        f"{user_stars}", False, (255, 132, 37)), (40, 8))


def menu(id):
    pix_Img = pygame.image.load(all_characters[id-1]["image"])
    pix_Img_big = pygame.image.load(all_characters[id-1]["image_big"])
    start_btn = pygame.image.load("play_btn.png")
    x = 0
    dx = 1
    running = True
    click = False
    while running:
        background(user_stars)
        mx, my = pygame.mouse.get_pos()
        btn = pygame.Rect(size[0]//2-start_btn.get_width()//2 + x,
                          size[1] // 3 + pix_Img.get_height(),
                          start_btn.get_width(),
                          start_btn.get_height()
                          )
        skin_btn = pygame.Rect(size[0]//2-skin_btn_img.get_width()//2, size[1]//3 + 250,
                               skin_btn_img.get_width(),
                               skin_btn_img.get_height())
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cur.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if btn.collidepoint((mx, my)):
            if click:
                platforms = [Platform(
                    data[i][0], data[i][1], data[i][2][0], data[i][2][1]) for i in range(2)]
                enemys = [Enemy(data[i][0], data[i][1], data[i]
                                [2][0], data[i][2][1]) for i in range(2, 5)]
                pygame.mixer.Sound.play(start_sound)
                game(pix_Img, pix_Img_big, 0, platforms, enemys, False, [])
                running = False
        if skin_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(press_sound)
                change_skin(id)
                running = False
        x += dx
        if x <= -25 or x >= 25:
            dx *= -1

        screen.blit(best_score_img, (size[0]//2-best_score_img.get_width() //
                                     2 + x, size[1]//3 - best_score_img.get_height() - 5))
        best_score = best_score_font.render(
            f"{user_best_score}", False, (255, 140, 16))
        screen.blit(best_score,
                    (size[0]//2 - best_score.get_width()//2 + x, size[1]//3 - best_score_img.get_height()))
        screen.blit(
            pix_Img, (size[0]//2-pix_Img.get_width()//2 + x, size[1]//3))
        screen.blit(start_btn, (size[0]//2-start_btn.get_width() //
                                2 + x, size[1]//3 + pix_Img.get_height()))
        screen.blit(
            skin_btn_img, (size[0]//2-skin_btn_img.get_width()//2, size[1]//3 + 250))
        pygame.display.flip()
        clock.tick(fps)


def change_skin(id):
    global user_stars
    running = True
    k = 0
    while running:
        background(user_stars)
        mx, my = pygame.mouse.get_pos()
        back_size = (size[0]//2-skin_back_img.get_width()//2,
                     size[1]//2 - skin_back_img.get_height()//2 - 50)

        right_btn = pygame.Rect(back_size[0]+skin_back_img.get_width()-skin_right_img.get_width(),
                                back_size[1]+skin_back_img.get_height()//2 -
                                skin_right_img.get_height()//2,
                                skin_right_img.get_width(),
                                skin_right_img.get_height())
        left_btn = pygame.Rect(back_size[0],
                               back_size[1]+skin_back_img.get_height()//2 -
                               skin_left_img.get_height()//2,
                               skin_right_img.get_width(),
                               skin_right_img.get_height())
        act_btn = pygame.Rect(size[0]//2-selected.get_width()//2, back_size[1] + 225,
                              selected.get_width(),
                              selected.get_height())

        exit_btn = pygame.Rect(size[0]//2-not_cont_img.get_width()//2, size[1]//2+cont.get_height()//2 - 40,
                               not_cont_img.get_width(),
                               not_cont_img.get_height())
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cur.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if right_btn.collidepoint((mx, my)):
            if click:
                if k < len(all_characters)-1:
                    k += 1
        elif left_btn.collidepoint((mx, my)):
            if click:
                if k > 0:
                    k -= 1

        skin = all_characters[k]

        if act_btn.collidepoint((mx, my)):
            if click:
                if skin["cost"] == 0 and skin["id"] == id:
                    pass
                elif skin["cost"] == 0 and skin["id"] != id:
                    pygame.mixer.Sound.play(press_sound)
                    id = skin["id"]
                    cur.execute('UPDATE User SET character_id = (?)', (id,))
                    conn.commit()
                else:
                    if user_stars >= skin["cost"]:
                        pygame.mixer.Sound.play(press_sound)
                        user_stars -= skin["cost"]
                        id = skin["id"]
                        skin["cost"] = 0
                        cur.execute(
                            'UPDATE User SET character_id = (?)', (id,))
                        cur.execute('UPDATE User SET stars = (?)',
                                    (user_stars,))
                        cur.execute(
                            'UPDATE Character SET cost = (?) WHERE id = (?)', (0, id))
                        conn.commit()
                    else:
                        pass
        if exit_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(press_sound)
                menu(id)
                running = False

        s = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 32))
        screen.blit(s, (0, 0))
        screen.blit(skin_back_img, back_size)
        screen.blit(skin_left_img, (back_size[0], back_size[1] +
                                    skin_back_img.get_height()//2-skin_left_img.get_height()//2))
        screen.blit(skin_right_img, (back_size[0]+skin_back_img.get_width()-skin_right_img.get_width(
        ), back_size[1]+skin_back_img.get_height()//2-skin_right_img.get_height()//2))
        skin_name = star_font.render(f"{skin['name']}", False, (255, 132, 37))
        screen.blit(
            skin_name, (size[0]//2-skin_name.get_width()//2, back_size[1] + 20))
        skin_img = pygame.image.load(skin['image_big'])
        screen.blit(
            skin_img, (size[0]//2-skin_img.get_width()//2, back_size[1] + 100))
        if skin["cost"] == 0:
            screen.blit(py_platform[1][0], (size[0]//2-py_platform[1]
                                            [0].get_width()//2, back_size[1] + 100 + skin_img.get_height()))
            if id == skin["id"]:
                screen.blit(
                    selected, (size[0]//2-selected.get_width()//2, back_size[1] + 225))
            else:
                screen.blit(
                    choose, (size[0]//2-choose.get_width()//2, back_size[1] + 225))
        else:
            screen.blit(buy_platform, (size[0]//2-buy_platform.get_width() //
                                       2, back_size[1] + 100 + skin_img.get_height()))
            if user_stars >= skin["cost"]:
                screen.blit(
                    buy, (size[0]//2-buy.get_width()//2, back_size[1] + 225))
            else:
                screen.blit(
                    cant_buy, (size[0]//2-cant_buy.get_width()//2, back_size[1] + 225))
        screen.blit(
            not_cont_img, (size[0]//2-not_cont_img.get_width()//2, size[1]//2+cont.get_height()//2 - 40))

        pygame.display.flip()
        clock.tick(fps)


def game(pix_Img, pix_Img_big, user_score, platforms, enemys, start=False, balls=[]):
    global user_best_score, user_stars
    pix_X = 100
    pix_Y = 0
    my_pix = Pix(pix_X, pix_Y, pix_Img)
    platforms[-1].trick = trick["star"]
    platforms[-1].trick_name = "star"
    running = True
    fall = False
    camera_fall = False
    bomb = False
    change = False
    click = False
    c = 0
    bar_size = (100, 8)
    bar_mushroom = (50, 8)
    bar_rect = pygame.Rect(size[0]//2-bar_size[0] //
                           2, 110, bar_size[0], bar_size[1])
    max_width = bar_size[0]-2
    max_width_m = bar_mushroom[0]-2
    min_time = 0
    time = 10
    time_m = 10
    coefficient = max_width / time
    coefficient_m = max_width_m / time_m
    dt = 0
    start_c = False
    temp = 0

    col_r, col_l = False, False
    spin = 0
    rot = False
    col_dead = False
    dead = False
    dead_cnt = 0
    dead_snd_was = False
    while running:
        click = False
        background(user_stars)
        if not rot:
            col = my_pix.collide(platforms[0])

        if my_pix.col_right(platforms[0]):
            col_r = True
            rot = True
            dead = True
            if not dead_snd_was:
                dead_snd_was = True
                pygame.mixer.Sound.play(dead_sound)
        if my_pix.col_left(platforms[0]):
            col_l = True
            rot = True
            dead = True
            if not dead_snd_was:
                dead_snd_was = True
                pygame.mixer.Sound.play(dead_sound)

        for i in range(len(enemys)):
            if my_pix.col_right(enemys[i]):
                col_r = True
                rot = True
                dead = True
                if not dead_snd_was:
                    dead_snd_was = True
                    pygame.mixer.Sound.play(dead_sound)
            if my_pix.col_left(enemys[i]):
                col_l = True
                rot = True
                dead = True
                if not dead_snd_was:
                    dead_snd_was = True
                    pygame.mixer.Sound.play(dead_sound)

        if col_r:
            spin += -4
            my_pix.x += 4
            my_pix.y += 6
            my_pix.image = pygame.transform.rotate(pix_dead_img, spin)
        if col_l:
            spin += +4
            my_pix.x -= 4
            my_pix.y += 6
            my_pix.image = pygame.transform.rotate(pix_dead_img, spin)

        for i in range(len(enemys)):
            if my_pix.collide_enemy(enemys[i]) and not rot and not dead:
                col_dead = True
                col_enemy = enemys[i]
                my_pix.image = pygame.transform.scale(pix_dead_img, (32, 24))
                dead = True
                pygame.mixer.Sound.play(dead_sound)
        if col_dead:
            my_pix.y = col_enemy.y-my_pix.height + 12
            my_pix.x += col_enemy.dx

        if my_pix.y > 700:
            dead = True
            dead_cnt = 60
            if not dead_snd_was:
                dead_snd_was = True
                pygame.mixer.Sound.play(dead_sound)

        if dead:
            dead_cnt += 1
            if dead_cnt >= 60:
                if user_score > user_best_score:
                    user_best_score = user_score
                    cur.execute('UPDATE User SET best_score = (?)',
                                (user_best_score,))
                cur.execute('UPDATE User SET stars = (?)', (user_stars,))
                conn.commit()
                if user_stars >= 100:
                    continue_game(pix_Img, pix_Img_big,
                                  user_score, platforms, enemys, balls)
                else:
                    pygame.mixer.Sound.play(restart_sound)
                    restart(pix_Img, pix_Img_big, user_score)
                running = False

        if col == False and not rot:
            my_pix.draw(size=(my_pix.width, my_pix.height + 16))
            my_pix.fall()
        elif col == True and fall == True and not rot:
            if platforms[0].trick_name == "star":
                user_stars += 1
                pygame.mixer.Sound.play(star_sound)
            elif platforms[0].trick_name == "green":
                pygame.mixer.Sound.play(ball_sound)
                balls.append((0, 255, 30))
            elif platforms[0].trick_name == "pink":
                pygame.mixer.Sound.play(ball_sound)
                balls.append((255, 0, 179))
            elif platforms[0].trick_name == "violet":
                pygame.mixer.Sound.play(ball_sound)
                balls.append((166, 0, 255))
            elif platforms[0].trick_name == "yellow":
                pygame.mixer.Sound.play(ball_sound)
                balls.append((255, 234, 0))
            elif platforms[0].trick_name == "leaf":
                pygame.mixer.Sound.play(trick_sound)
            elif platforms[0].trick_name == "mushroom":
                pygame.mixer.Sound.play(trick_sound)
                my_pix = Pix(my_pix.x, my_pix.y, pix_Img_big)
                change = True
                time_m = 10
            elif platforms[0].trick_name == "carrot":
                pygame.mixer.Sound.play(trick_sound)
            else:
                pygame.mixer.Sound.play(fall_sound)
            user_score += 1
            Platform.cnt = 0
            Platform.sz = 0
            fall = False
            update_platform(platforms, enemys)
            my_pix.draw()
            time = 10
            start = True
        else:
            my_pix.draw()
            if temp == 0:
                pygame.mixer.Sound.play(fall_sound)
                temp = 1
            start_c = True
            if start == True:
                if time > min_time:
                    time -= dt
        if change == True:
            if time_m > min_time:
                time_m -= dt
        for i in range(len(platforms)):
            platforms[i].move()
            if platforms[i].opacity == 0:
                platforms[i].draw()
            else:
                platforms[i].draw_alpha()
        platforms[-1].draw_smth(platforms[-1].trick)
        for i in range(len(enemys)):
            enemys[i].move()
            if enemys[i].opacity == 0:
                enemys[i].draw()
            else:
                enemys[i].draw_alpha()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cur.close()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu(cur.execute(
                        'SELECT character_id FROM User').fetchone()[0])
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    # fall = True
                    # del platforms[0]
                    # my_pix.fall()
                    # camera_fall = True
                    # c = c - 40
                # if event.button == 3 and user_stars>=10:
                #     user_stars -= 10
                #     del platforms[-1]
                #     update_platform(platforms, enemys)
                #     camera_fall = True
                #     bomb = True
                #     c = c - 40
                #     time = 10

        mx, my = pygame.mouse.get_pos()
        bomb_btn = pygame.Rect(
            20, size[1]-bomb_img.get_height()-70, bomb_img.get_width(),  bomb_img.get_height())
        if start_c == False:
            click = False
            my_pix.image = pix_Img
        if click:
            if bomb_btn.collidepoint((mx, my)) and user_stars >= 10:
                if my_pix.collide(platforms[0]) and camera_fall == False:
                    user_stars -= 10
                    del platforms[-1]
                    pygame.mixer.Sound.play(drop_sound)
                    update_platform(platforms, enemys)
                    camera_fall = True
                    bomb = True
                    c = c - 40
                    time = 10
            else:
                fall = True
                del platforms[0]
                pygame.mixer.Sound.play(drop_sound)
                my_pix.fall()
                camera_fall = True
                c = c - 40

        if time_m <= 0 and change == True:
            my_pix = Pix(my_pix.x, my_pix.y, pix_Img)
            change = False

        if time <= 0 and fall == False:
            fall = True
            del platforms[0]
            pygame.mixer.Sound.play(drop_sound)
            my_pix.fall()
            camera_fall = True
            c = c - 40

        if camera_fall:
            dy = 3
            my_pix.y -= dy
            if bomb:
                platforms[-1].y -= dy
            else:
                for i in range(len(platforms)):
                    platforms[i].y -= dy
            for i in range(len(enemys)):
                enemys[i].y -= dy
            c += 1
            if c == 0:
                camera_fall = False
                bomb = False

        score_txt = font.render(f"{user_score}", False, (255, 255, 255))
        score_txt_b = bord.render(f"{user_score}", False, (47, 109, 246))
        screen.blit(score_txt, (size[0]//2-score_txt.get_width()//2, 30))
        screen.blit(score_txt_b, (size[0]//2-score_txt_b.get_width()//2, 30))
        width = time * coefficient
        width_m = time_m * coefficient_m
        pygame.draw.rect(screen, (118, 200, 250),
                         (size[0]//2-bar_size[0]//2 - 3, 110 - 3, bar_size[0]+6, bar_size[1]+6))
        pygame.draw.rect(screen, (212, 246, 254),
                         (size[0]//2-bar_size[0]//2 - 2, 110 - 2, bar_size[0]+4, bar_size[1]+4))
        pygame.draw.rect(screen, (47, 109, 246), bar_rect)
        pygame.draw.rect(screen, (249, 229, 106),
                         (size[0]//2-bar_size[0]//2 + 1, 110 + 1, width, bar_size[1]-2))
        screen.blit(bomb_img, (20, size[1]-bomb_img.get_height()-70))
        if len(balls) > 3:
            balls.pop(0)
        if len(balls) == 3 and len(set(balls)) == 1:
            pygame.mixer.Sound.play(bonus_sound)
            bonus_raund(pix_Img, pix_Img_big, user_score-1, balls[0])
            running = False
        for i in range(3):
            try:
                pygame.draw.circle(screen, balls[i], (size[0]+26*i-80, 26), 12)
            except:
                pygame.draw.circle(screen, (0, 0, 0),
                                   (size[0]+26*i-80, 26), 12, 1)

        if change == True:
            screen.blit(mushroom, (370, 50))
            bar_mushroom_rect = pygame.Rect(
                4*size[0]//5-bar_size[0]//2+50, 90, bar_mushroom[0], bar_mushroom[1])
            pygame.draw.rect(screen, (118, 200, 250), (
                4*size[0]//5-bar_size[0]//2 + 50 - 3, 90 - 3, bar_mushroom[0]+6, bar_mushroom[1]+6))
            pygame.draw.rect(screen, (212, 246, 254), (
                4*size[0]//5-bar_size[0]//2 + 50 - 2, 90 - 2, bar_mushroom[0]+4, bar_mushroom[1]+4))
            pygame.draw.rect(screen, (47, 109, 246), bar_mushroom_rect)
            pygame.draw.rect(screen, (249, 229, 106), (
                4*size[0]//5-bar_size[0]//2 + 50 + 1, 90 + 1, width_m, bar_mushroom[1]-2))

        pygame.display.flip()
        dt = clock.tick(fps)/500


def update_platform(platforms, enemys):
    spec_case = rand(0, 15)
    if 'long' in enemys[0].picname:
        image = py_platform[0]
    elif 'short' in enemys[0].picname:
        image = py_platform[1]
    if spec_case == 1:
        choose = "leaf"
    elif spec_case == 2:
        choose = "mushroom"
    elif spec_case == 3:
        choose = "carrot"
    elif spec_case == 4:
        choose = "green"
    elif spec_case == 5:
        choose = "pink"
    elif spec_case == 6:
        choose = "violet"
    elif spec_case == 7:
        choose = "yellow"
    else:
        choose = "star"
    platforms.append(Platform(enemys[0].x, enemys[0].y, image[0], image[1],
                              enemys[0].dx, enemys[0].special, enemys[0].opacity, 2, trick[choose], choose))
    platforms[-1].dx = enemys[0].dx
    del enemys[0]
    new = data[rand(2, 4)]
    if spec_case == 8:
        enemys.append(Enemy(new[0], enemys[-1].y +
                            120, new[2][0], new[2][1], 10))
    elif spec_case == 9:
        enemys.append(Enemy(new[0], enemys[-1].y+120,
                            new[2][0], new[2][1], 3, True))
    elif spec_case == 10:
        enemys.append(Enemy(new[0], enemys[-1].y+120,
                            new[2][0], new[2][1], 3, False, 20))
    elif spec_case == 11:
        enemys.append(Enemy(new[0], enemys[-1].y+120,
                            new[2][0], new[2][1], 3, False, 0, 2, True))
    else:
        enemys.append(Enemy(new[0], enemys[-1].y+120, new[2][0], new[2][1]))


def restart(pix, pix_Img_big, score):
    global user_best_score, user_stars
    running = True
    while running:
        background(user_stars)
        mx, my = pygame.mouse.get_pos()
        restart_btn = pygame.Rect(size[0]//2-restart_btn_img.get_width()//2, size[1]//2-restart_btn_img.get_height()//2,
                                  restart_btn_img.get_width(),
                                  restart_btn_img.get_height())
        home_btn = pygame.Rect(
            size[0]-home.get_width()-10, 10, home.get_width(), home.get_height())
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cur.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if restart_btn.collidepoint((mx, my)):
            if click:
                platforms = [Platform(
                    data[i][0], data[i][1], data[i][2][0], data[i][2][1]) for i in range(2)]
                enemys = [Enemy(data[i][0], data[i][1], data[i]
                                [2][0], data[i][2][1]) for i in range(2, 5)]
                pygame.mixer.Sound.stop(restart_sound)
                pygame.mixer.Sound.play(start_sound)
                game(pix, pix_Img_big, 0, platforms, enemys, False, [])
                running = False
        if home_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(start_sound)
                menu(cur.execute(
                    'SELECT character_id FROM User').fetchone()[0])
                running = False
        score_f = star_font.render(f"score", False, (47, 109, 246))
        user_score = font.render(f"{score}", False, (47, 109, 246))
        best_score = star_font.render(
            f"best: {user_best_score}", False, (255, 140, 16))
        screen.blit(
            score_f, (size[0]//2 - score_f.get_width()//2, size[1]//2 - 225))
        screen.blit(
            user_score, (size[0]//2 - user_score.get_width()//2, size[1]//2 - 200))
        screen.blit(
            best_score, (size[0]//2 - best_score.get_width()//2, size[1]//2 - 125))
        screen.blit(restart_btn_img,  (size[0]//2-restart_btn_img.get_width(
        )//2, size[1]//2-restart_btn_img.get_height()//2))
        screen.blit(home, (size[0]-home.get_width()-10, 10))
        pygame.display.flip()
        clock.tick(fps)


def continue_game(pix, pix_Img_big, score, platforms, enemys, balls):
    global user_best_score, user_stars
    running = True
    while running:
        background(user_stars)
        mx, my = pygame.mouse.get_pos()
        cont_btn = pygame.Rect(size[0]//2-cont_btn_img.get_width()//2, size[1]//2-cont.get_height()//2 + 150,
                               cont_btn_img.get_width(),
                               cont_btn_img.get_height())
        not_cont_btn = pygame.Rect(size[0]//2-not_cont_img.get_width()//2, size[1]//2+cont.get_height()//2 - 40,
                                   not_cont_img.get_width(),
                                   not_cont_img.get_height())
        click = False

        for i in range(len(platforms)):
            platforms[i].move()
            platforms[i].draw()
        for i in range(len(enemys)):
            enemys[i].move()
            enemys[i].draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cur.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if cont_btn.collidepoint((mx, my)):
            if click:
                user_stars -= 100
                cur.execute('UPDATE User SET stars = (?)', (user_stars,))
                conn.commit()
                platforms = [Platform(
                    data[i][0], data[i][1], data[i][2][0], data[i][2][1]) for i in range(2)]
                enemys = [Enemy(data[i][0], data[i][1], data[i]
                                [2][0], data[i][2][1]) for i in range(2, 5)]
                pygame.mixer.Sound.play(start_sound)
                game(pix, pix_Img_big, score, platforms, enemys, True, balls)
                running = False
        elif not_cont_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(restart_sound)
                restart(pix, pix_Img_big, score)
                running = False

        s = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 32))
        screen.blit(s, (0, 0))
        screen.blit(cont, (size[0]//2-cont.get_width() //
                           2, size[1]//2-cont.get_height()//2 - 50))
        best_score = star_font.render(
            f"best score {user_best_score}", False, (255, 140, 16))
        screen.blit(best_score,
                    (size[0]//2 - best_score.get_width()//2, size[1]//2-cont.get_height()//2 + 100))
        screen.blit(
            cont_btn_img,  (size[0]//2-cont_btn_img.get_width()//2, size[1]//2-cont.get_height()//2 + 150))
        screen.blit(
            not_cont_img, (size[0]//2-not_cont_img.get_width()//2, size[1]//2+cont.get_height()//2 - 40))

        pygame.display.flip()
        clock.tick(fps)


def bonus_raund(pix, pix_big, user_score, color):
    global user_stars
    my_pix = Pix((size[0]//2)-(pix_big.get_width()//2), 0, pix_big)
    running = True
    camera_fall = False
    c = 0
    bar_size = (100, 8)
    bar_rect = pygame.Rect(size[0]//2-bar_size[0] //
                           2, 110, bar_size[0], bar_size[1])
    max_width = bar_size[0]-2
    min_time = 0
    time = 10
    coefficient = max_width / time
    dt = 0
    alpha = 2
    opacity = 4
    s = pygame.Surface(size).convert()
    platforms = [Platform(0, 200+(dst*i), bonus_platform, None, 0)
                 for i in range(2)]
    enemys = [Enemy(0, 200+(dst*i), bonus_kill, None, 0) for i in range(2, 5)]
    fall = False
    font_for_bonus = pygame.font.Font('Jesus_Heals.ttf', 120)
    bord_for_bonus = pygame.font.Font('Jesus_Lives.ttf', 120)
    bonus_txt = font_for_bonus.render("bonus!",  False, (255, 255, 0))
    bonus_txt_b = bord_for_bonus.render("bonus!", False, (247, 74, 0))
    start = False
    zoom = 0
    cnt = 0
    while running:
        screen.fill((255, 255, 255))
        opacity += alpha
        if opacity >= 155 or opacity <= 4:
            alpha *= -1
        s.blit(screen, (-0, -0))
        s.fill(color)
        s.set_alpha(opacity)
        screen.blit(s, (0, 0))
        col = my_pix.collide(platforms[0])
        if col == False:
            my_pix.draw((my_pix.width, my_pix.height+20))
            my_pix.fall()
        elif col == True and fall == True:
            pygame.mixer.Sound.play(bonus_star_sound)
            user_stars += 5
            user_score += 1
            platforms.append(Platform(0, enemys[0].y, bonus_platform, None, 0))
            del enemys[0]
            enemys.append(Enemy(0, enemys[-1].y+120, bonus_kill, None, 0))
            fall = False
            Platform.sz = 0
            Platform.cnt = 0
        else:
            my_pix.draw()

        if start == True and time > min_time:
            time -= dt

        for i in range(len(platforms)):
            platforms[i].draw()

        platforms[-1].draw_smth(star_rainbow)

        for i in range(len(enemys)):
            enemys[i].draw()
            enemys[i].draw_smth(star_rainbow)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cur.close()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu(cur.execute(
                        'SELECT character_id FROM User').fetchone()[0])
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(platforms) == 2 and start == True:
                        fall = True
                        del platforms[0]
                        my_pix.fall()
                        camera_fall = True
                        c = c - 20

        if time <= 0:
            cur.execute('UPDATE User SET stars = (?)', (user_stars,))
            conn.commit()
            platforms = [Platform(
                data[i][0], data[i][1], data[i][2][0], data[i][2][1]) for i in range(2)]
            enemys = [Enemy(data[i][0], data[i][1], data[i][2]
                            [0], data[i][2][1]) for i in range(2, 5)]
            game(pix, pix_big, user_score, platforms, enemys, True, [])
            running = False

        if camera_fall:
            dy = 6
            my_pix.y -= dy
            for i in range(len(platforms)):
                platforms[i].y -= dy
            for i in range(len(enemys)):
                enemys[i].y -= dy
            c += 1
            if c == 0:
                camera_fall = False
        if start == False:
            if zoom < bonus_txt.get_width():
                screen.blit(pygame.transform.scale(
                    bonus_txt, (zoom, bonus_txt.get_height())), (size[0]//2-zoom//2, size[1]//3))
                screen.blit(pygame.transform.scale(
                    bonus_txt_b, (zoom, bonus_txt_b.get_height())), (size[0]//2-zoom//2, size[1]//3))
            else:
                cnt += 10
                screen.blit(
                    bonus_txt, (size[0]//2-bonus_txt.get_width()//2-cnt, size[1]//3))
                screen.blit(
                    bonus_txt_b, (size[0]//2-bonus_txt_b.get_width()//2-cnt, size[1]//3))
                if size[0]//2-bonus_txt.get_width()//2-cnt < -bonus_txt.get_width():
                    start = True
            zoom += 10

        screen.blit(pygame.transform.scale(star, (28, 28)), (10, 10))
        screen.blit(star_font.render(
            f"{user_stars}", False, (255, 132, 37)), (40, 8))
        score_txt = font.render(f"{user_score}", False, (255, 255, 255))
        score_txt_b = bord.render(f"{user_score}", False, (47, 109, 246))
        screen.blit(score_txt, (size[0]//2-score_txt.get_width()//2, 30))
        screen.blit(score_txt_b, (size[0]//2-score_txt_b.get_width()//2, 30))
        width = time * coefficient
        pygame.draw.rect(screen, (118, 200, 250),
                         (size[0]//2-bar_size[0]//2 - 3, 110 - 3, bar_size[0]+6, bar_size[1]+6))
        pygame.draw.rect(screen, (212, 246, 254),
                         (size[0]//2-bar_size[0]//2 - 2, 110 - 2, bar_size[0]+4, bar_size[1]+4))
        pygame.draw.rect(screen, (47, 109, 246), bar_rect)
        pygame.draw.rect(screen, (249, 229, 106),
                         (size[0]//2-bar_size[0]//2 + 1, 110 + 1, width, bar_size[1]-2))
        pygame.display.flip()
        dt = clock.tick(fps)/500


menu(character_id)
pygame.quit()
cur.close()
