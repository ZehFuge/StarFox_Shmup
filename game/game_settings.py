# library import block
from os import path
from sys import exit
from random import randrange
from random import choice
from random import randint
from random import random
import pygame


# library init block
pygame.mixer.init()
pygame.font.init()


# game information block
# game settings
WIDTH = 1200
HEIGHT = 800
# HALF_WIDHT is needed for multiple laser display
HALF_WIDHT = WIDTH / 2
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# fonts needs to be pre declared, to blit text on surface through function
font_name = pygame.font.match_font("Arial")
# needs to set skins for the enemy sprites withouth random
enemy_img_counter = 0

# pre defined colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CONVERT_SCORE = (89, 193, 53)
CONVERT_WINGS = (172, 50, 50)
CONVERT_PLAYER = (181, 230, 29)


# last_updates
last_update = {}
last_update["more_villans"] = pygame.time.get_ticks()


# image loading block
# save image and sound folder dir to var
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

# load pictures and make them transparent
# images need to be converted by convert(), if not, the frame rate will suffer due to calculation
player_imgs = {}
player_imgs["idle"] = pygame.image.load(path.join(img_dir, "arwing_idle_rgb_181_230_29.png")).convert()
player_imgs["idle"].set_colorkey(CONVERT_PLAYER)

player_imgs["left"] = pygame.image.load(path.join(img_dir, "arwing_left_rgb_181_230_29.png")).convert()
player_imgs["left"].set_colorkey(CONVERT_PLAYER)

player_imgs["right"] = pygame.image.load(path.join(img_dir, "arwing_right_rgb_181_230_29.png")).convert()
player_imgs["right"].set_colorkey(CONVERT_PLAYER)

# set player lives image
player_live_img = player_imgs["idle"]

# resize the player sprite after copying as mini format for lives display
# resize the player sprite: pygame.transform.scale(image, (new_width, new_height))
player_imgs["idle"] = pygame.transform.scale(player_imgs["idle"], (96, 96))
player_imgs["left"] = pygame.transform.scale(player_imgs["left"], (96, 96))
player_imgs["right"] = pygame.transform.scale(player_imgs["right"], (96, 96))

# load background image
background_img = pygame.image.load(path.join(img_dir, "space_background_1200x800_nsm.png")).convert()
background_img_rect = background_img.get_rect()

# load laser images
green_laser = pygame.image.load(path.join(img_dir, "green_laser_15x25p_rgb_black.png")).convert()
green_laser.set_colorkey(BLACK)
blue_laser = pygame.image.load(path.join(img_dir, "blue_laser_15x25p_rgb_black.png")).convert()
blue_laser.set_colorkey(BLACK)
red_laser = pygame.image.load(path.join(img_dir, "red_laser_15x25p_rgb_black.png")).convert()
red_laser.set_colorkey(BLACK)

# loading meteor image
# the colorkey is set in the class Meteors
meteor_images = []
meteor_images_list = ["meteor_64x64p_rgb_0_0_0.png",
                      "meteor_96x96p_rgb_0_0_0.png",
                      "meteor_128x128p_rgb_0_0_0.png"]
# load all images in meteor_images list
for img in meteor_images_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# load enemy images
enemy_imgs = {}

enemy_imgs[0] = pygame.image.load(path.join(img_dir, "enemy1_r181_g230_b29.png")).convert()
enemy_imgs[0] = pygame.transform.scale(enemy_imgs[0], (96, 96))
enemy_imgs[0].set_colorkey(CONVERT_PLAYER)

enemy_imgs[1] = pygame.image.load(path.join(img_dir, "enemy2_r181_g230_b29.png")).convert()
enemy_imgs[1] = pygame.transform.scale(enemy_imgs[1], (96, 96))
enemy_imgs[1].set_colorkey(CONVERT_PLAYER)

enemy_imgs[2] = pygame.image.load(path.join(img_dir, "enemy3_r181_g230_b29.png")).convert()
enemy_imgs[2] = pygame.transform.scale(enemy_imgs[2], (96, 96))
enemy_imgs[2].set_colorkey(CONVERT_PLAYER)

enemy_imgs[3] = pygame.image.load(path.join(img_dir, "enemy4_r181_g230_b29.png")).convert()
enemy_imgs[3] = pygame.transform.scale(enemy_imgs[3], (96, 96))
enemy_imgs[3].set_colorkey(CONVERT_PLAYER)

enemy_imgs[4] = pygame.image.load(path.join(img_dir, "enemy5_r181_g230_b29.png")).convert()
enemy_imgs[4] = pygame.transform.scale(enemy_imgs[4], (96, 96))
enemy_imgs[4].set_colorkey(CONVERT_PLAYER)

# load score surface image
score_image = pygame.image.load(path.join(img_dir, "score_display0_32x128_rgb_89_193_53.png")).convert()
score_image = pygame.transform.scale(score_image, (256, 64))
score_image.set_colorkey(CONVERT_SCORE)
score_image_rect = score_image.get_rect()

# load muliplicator surface image
multi_image = pygame.image.load(path.join(img_dir, "multiplicator_display0_32x32p_rgb_89_193_53.png")).convert()
multi_image = pygame.transform.scale(multi_image, (64, 64))
multi_image.set_colorkey(CONVERT_SCORE)
multi_image_rect = multi_image.get_rect()


# load power up images
power_up_images = {}
power_up_images["wings"] = pygame.image.load(path.join(img_dir, "wings_power_up_32x32p_rgb_172_50_50.png")).convert()
power_up_images["wings"].set_colorkey(CONVERT_WINGS)
power_up_images["wings"] = pygame.transform.scale(power_up_images["wings"], (64, 64))

power_up_images["double"] = pygame.image.load(path.join(img_dir, "multiplicator_power_up_32x32p_rgb_white.png")).convert()
power_up_images["double"].set_colorkey(WHITE)
power_up_images["double"] = pygame.transform.scale(power_up_images["double"], (64, 64))

power_up_images["silver"] = pygame.image.load(path.join(img_dir, "silver_ring_power_up_32x32p_rgb_white.png")).convert()
power_up_images["silver"].set_colorkey(WHITE)
power_up_images["silver"] = pygame.transform.scale(power_up_images["silver"], (64, 64))

power_up_images["gold"] = pygame.image.load(path.join(img_dir, "gold_ring_power_up_32x32p_rgb_white.png")).convert()
power_up_images["gold"].set_colorkey(WHITE)
power_up_images["gold"] = pygame.transform.scale(power_up_images["gold"], (64, 64))


# load explosions images
explosion_animation = {}
explosion_animation["lg"] = [] # lg = large explosion
explosion_animation["sm"] = [] # sm = small explosion
explosion_animation["player"] = []

for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion_animation["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation["sm"].append(img_sm)

    filename = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation["player"].append(img)


# sounds loading block
# load game theme
game_music = pygame.mixer.music.load(path.join(snd_dir, "corneria_theme_music.mp3"))
# set game_music loudness
pygame.mixer.music.set_volume(0.1) # 0.3
# set game_music to inifinit loop
pygame.mixer.music.play(loops=-1)

# load shooting sounds
laser_sound = {}
laser_sound[0] = pygame.mixer.Sound(path.join(snd_dir, "single_laser_sfx.ogg"))
laser_sound[0].set_volume(0.3)

laser_sound[1] = pygame.mixer.Sound(path.join(snd_dir, "dual_laser_sfx.ogg"))
laser_sound[1].set_volume(0.3)

laser_sound[2] = pygame.mixer.Sound(path.join(snd_dir, "tripple_laser_sfx.ogg"))
laser_sound[2].set_volume(0.3)

# load power up sounds
power_up_sound = {}
power_up_sound["rings"] = pygame.mixer.Sound(path.join(snd_dir, "power_up_ring.ogg"))
power_up_sound["rings"].set_volume(0.2)

power_up_sound["wings"] = pygame.mixer.Sound(path.join(snd_dir, "power_up_wings.ogg"))
power_up_sound["wings"].set_volume(0.2)

power_up_sound["double"] = pygame.mixer.Sound(path.join(snd_dir, "power_up_multi.ogg"))
power_up_sound["double"].set_volume(0.7)


# load explosion sound
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, "explosion_sfx.ogg"))
explosion_sound.set_volume(0.1)


# declare sprite groups
# and declare all_sprite variable
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
enemys = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


# sprite classes and function block
# definition of the Player class
class Player(pygame.sprite.Sprite):
    # init the class
    def __init__(self):
        # init the sprite
        pygame.sprite.Sprite.__init__(self)
        # set player image and get its rect to work
        self.image = player_imgs["idle"]
        self.rect = self.image.get_rect()

        # set start position for the player sprite
        # middle of the bottom screen
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = background_img_rect.bottom - 5


        # player information block
        self.move_speed = 0
        # declare a delay for shooting to provide non stop fire
        # this will be used with the time function and the last_shot variable
        # in this case 250 = milliseconds
        self.shoot_delay = 250
        self.last_shot = 0
        self.lives = 3
        # shield is used as the players hp bar
        self.shield = 100

        self.radius = int(self.rect.width / 2.2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        # create a score counter for the player and a multiplier for more visual fun
        self.score = 0
        self.score_multiplier = 1
        # the hurt_mode allows to take damage. It is used for delay
        # otherwise player could lose all life by impact of multiple spritecollides at once
        self.hurt_mode = True
        self.hurt_delay = 520
        self.last_update = pygame.time.get_ticks()
        # hides the sprite of the player if player loses a life
        self.hide = False
        # power level defines the strength of the laser
        self.power_level = 1


    # update the player sprite by user input
    def update(self):
        # save the input in a variable for better movement controls
        keystate = pygame.key.get_pressed()

        # checker for user input for movement
        # also check if player trys to leave the screen
        if keystate[pygame.K_a] \
                or keystate[pygame.K_LEFT]:
            self.image = player_imgs["left"]
            self.move_speed = -10
            # wall check screen.left
            if (self.rect.left + self.move_speed) > 0:
                self.rect.x += self.move_speed

        if keystate[pygame.K_d] \
                or keystate[pygame.K_RIGHT]:
            self.image = player_imgs["right"]
            self.move_speed = 10
            # wall check screen.right
            if (self.rect.right + self.move_speed) < WIDTH:
                self.rect.x += self.move_speed

        if keystate[pygame.K_w] \
                or keystate[pygame.K_UP]:
            self.move_speed = -7
            # wall check screen.top
            if (self.rect.top + self.move_speed) > 0:
                self.rect.y += self.move_speed

        if keystate[pygame.K_s] \
                or keystate[pygame.K_DOWN]:
            self.move_speed = 7
            # wall check screen.bottom
            if (self.rect.bottom + self.move_speed) < HEIGHT:
                self.rect.y += self.move_speed

        if keystate[pygame.K_SPACE]:
            self.shoot()

        # reset player image if a or d got released
        if not keystate[pygame.K_a]:
            if not keystate[pygame.K_d]:
                self.image = player_imgs["idle"]

    # make the player shoot after pressing the space bar
    def shoot(self):
        # set the time of pressing space to a variable
        now = pygame.time.get_ticks()

        # if enough time passed since the last shot, shoot again
        if now - self.last_shot > self.shoot_delay:
            # if enough time has passed, set new time for last_shot variable
            self.last_shot = now

            # laser object amount is declared by the power_level of the player
            # single shot
            if player.power_level == 1:
                # give the class the needed information to create bullet object
                # information are given by rect information of the sprite
                bullet1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                laser_sound[0].play()
                bullets.add(bullet1)

            # double shot
            if player.power_level == 2:
                bullet1 = Bullet(self.rect.centerx - (self.rect.width / 2), self.rect.top)
                bullet2 = Bullet(self.rect.centerx + (self.rect.width / 2), self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                laser_sound[1].play()

            # tripple shot
            if player.power_level >= 3:
                bullet0 = Bullet(self.rect.centerx, self.rect.top - 50)
                bullet1 = Bullet(self.rect.centerx - (self.rect.width / 2), self.rect.top)
                bullet2 = Bullet(self.rect.centerx + (self.rect.width / 2), self.rect.top)
                all_sprites.add(bullet0)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet0)
                bullets.add(bullet1)
                bullets.add(bullet2)
                laser_sound[2].play()


    # this function activates to avoid taking multiple damage at once
    # through multiple sprite collisions
    def hurt(self):
        now = pygame.time.get_ticks()
        if self.hurt_mode:
            self.last_update = now
            if self.shield <= 0:
                # create explosion image and play its sound
                explosion = Explosion(self.rect.center, "player")
                all_sprites.add(explosion)
                explosion_sound.play()

                self.lives -= 1
                # reset multiplier bonus
                self.score_multiplier = 1
                # reset the power level of the weapon
                self.power_level = 1
                self.shield = 100
                self.hide = True
                # set hurt_mode to false, to avoid damage for a short time
                self.hurt_mode = False
                if self.lives == 0:
                        display_game_over()
            else:
                # player takes damage
                self.shield -= 20
                # reset multiplier bonus
                self.score_multiplier = 1

        if not self.hurt_mode:
            if now - self.last_update > int(self.hurt_delay):
                self.hurt_mode = True
                self.hide = False
                now = pygame.time.get_ticks()


# create player object and add it to the right sprite groups
player = Player()
all_sprites.add(player)
players.add(player)


# class for spawning bullets and their behavior
class Bullet(pygame.sprite.Sprite):
    # bullets need the coordinates of the player sprite as spawn position
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # set image to sprite and get its rectangle information
        if player.power_level == 1:
            self.image = green_laser
        if player.power_level >= 2:
            self.image = blue_laser
        self.rect = self.image.get_rect()

        # set spawn position by player coordiantes
        self.rect.bottom = y
        self.rect.centerx = x
        # the speed is subtrakted because the bullet is flying up
        self.move_speed = -20

    # set the update information for behavior
    def update(self):
        # set movement decided by move_speed
        self.rect.y += self.move_speed

        # if the bottom part of the sprites leaves the upper window range (x = 0), destroy it
        if self.rect.bottom < 0:
            self.kill()


# class for randomly spawning meteors
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # select random size meteor
        # 64x64p, 96x96p or 128x128p
        self.image_original = choice(meteor_images)
        self.image_original.set_colorkey(WHITE)

        # further information needed to rotate the image
        # creates a more dynamic gameplay
        self.image = self.image_original.copy()
        # for right sprite display, the rect argument always needs to be self.rect
        self.rect = self.image.get_rect()
        # let each object rotate in a different speed for more realistic feeling
        self.rotation = 0
        self.rotation_speed = randrange(-15, 15)
        # denie rotation_speed = 0
        while self.rotation_speed == 0:
            self.rotation_speed = randrange(-15, 15)
        self.last_update = pygame.time.get_ticks()

        # set start randomly generated start positons
        self.rect.x = randrange(0, WIDTH - self.rect.width)
        # start position y set to negative, so it doesnt pop up on screen but comes in naturally
        self.rect.y = randrange(-150, -100)

        # set fly behavior
        self.speed_y = randrange(8, 15)
        self.speed_x = randrange(-3, 3)

        # create circular hitbox
        self.radius = int(self.rect.width / 2.2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    # make the sprite rotate
    def rotate(self):
        now = pygame.time.get_ticks()
        # rotate spirte every 50 milliseconds
        if now - self.last_update > 50:
            self.last_update = now
            # calculate rotation angle
            self.rotation = (self.rotation + self.rotation_speed) % 360
            # pygame.transform.rotate(surface, angle)
            new_image = pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    # update position by behavior
    def update(self):
        # Test with fixed and visible position
        # self.rect.x = 50
        # self.rect.y = 100

        # rotate the sprite
        self.rotate()

        # move the meteor
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # check if meteor left the screen -> respawn if true
        if self.rect.top > HEIGHT \
                or self.rect.left < (0 - self.rect[2]) \
                or self.rect.right > (WIDTH + self.rect[2]):
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-150, -100)
            self.speed_y = randrange(4, 8)
            self.speed_x = randrange(-2, 2)


# class for enemy bullets which fly downwards
class Enemy_Bullet(pygame.sprite.Sprite):
    # bullets need the coordinates of the player sprite as spawn position
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # set image to sprite and get its rectangle information
        self.image = red_laser
        self.rect = self.image.get_rect()

        # set spawn position by player coordiantes
        self.rect.bottom = y
        self.rect.centerx = x
        # the speed is subtrakted because the bullet is flying up
        self.move_speed = 8

    # set the update information for behavior
    def update(self):
        # set movement decided by move_speed
        self.rect.y += self.move_speed

        # if the bottom part of the sprites leaves the bottom window range, destroy it
        if self.rect.top > HEIGHT:
            self.kill()


# class for random spawning enemys
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global enemy_img_counter

        # set random sprite image defined by enemy_imgs dictonary
        # self.image_type = choice(["first", "second", "third", "fourth", "fifth"])
        # self.image = enemy_imgs[self.image_type]
        if enemy_img_counter > 4:
            enemy_img_counter = 0
        self.image = enemy_imgs[enemy_img_counter]
        enemy_img_counter += 1
        self.rect = self.image.get_rect()

        # save time, so every 3 seconds the enemy will shoot
        self.last_shot = pygame.time.get_ticks()
        self.shooting_delay = randrange(1000, 3000)

        # information needed for movement and hitbox
        self.radius = self.rect.width / 2.5
        self.speed_y = randrange(1, 5)

        # set start randomly generated start positons
        self.rect.x = randrange(0, WIDTH - self.rect.width)
        # start position y set to negative, so it doesnt pop up on screen but comes in naturally
        self.rect.y = -100

    def update(self):
        # move enemys y-axis by speed_y value
        self.rect.y += self.speed_y

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shooting_delay:
            self.last_shot = now
            self.shoot()

        if self.rect.top > HEIGHT \
                or self.rect.left < (0 - self.rect[2]) \
                or self.rect.right > (WIDTH + self.rect[2]):
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-150, -100)
            self.speed_y = randrange(1, 5)
            self.speed_x = randrange(-2, 2)

    def shoot(self):
        # give the class the needed information to create bullet object
        # information are given by rect information of the sprite
        bullet1 = Enemy_Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet1)
        laser_sound[0].play()
        enemy_bullets.add(bullet1)


# power up object definition and dropchances
class Power_Ups(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # set drop chances for items to avoid an OP player at the begining
        self.drop_chance = random()
        if self.drop_chance <= 0.4: # 40%
            self.type = "silver"
        if 0.4 < self.drop_chance < 0.7: # 30%
            self.type = "wings"
        if 0.7 < self.drop_chance < 0.9: # 20%
            self.type = "double"
        if self.drop_chance >= 0.9: # 10%
            self.type = "gold"

        self.image = power_up_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        # kill if it leaves the screen
        if self.rect.top > HEIGHT:
            self.kill()


# creates explosion images
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20

    def update(self):
        # save new time
        now = pygame.time.get_ticks()
        # if 20ms have passed, set new image frame
        if (now - self.last_update) > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # if the last frame is reached, kill the object
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def end_game():
    quit()
    exit()


def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)


# function to write text on surfaces
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# draws the already achieved score by the player
def draw_score():
    screen.blit(score_image, (5, 5))
    draw_text(screen, str(player.score), 38, WHITE, (score_image_rect.width / 2), (score_image_rect.y + 25))

# draw the multiplicator of the player
def draw_multi():
    multi_image_rect.x = score_image_rect.width + 10
    multi_image_rect.y = 5
    screen.blit(multi_image, (multi_image_rect.x, 5))
    draw_text(screen, str(player.score_multiplier), 38, WHITE, (multi_image_rect.x + (multi_image_rect.width / 2)), (multi_image_rect.y + 20))

# draw the hp bar of the player
def draw_shield_bar(surface, x, y, shield):
    if shield < 0:
        shield = 0
    # set size for the hp bar
    BAR_LENGTH = 200
    BAR_HEIGHT = 30
    # if shield gets lower, the shield bar will decrease in length
    fill = (shield / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    outline_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    # draw the hp bar
    pygame.draw.rect(surface, GREEN, fill_rect)
    # draw the outline of the hp bar
    pygame.draw.rect(surface, WHITE, outline_rect, 1)


def display_welcome():
    screen.blit(background_img, background_img_rect)
    draw_text(screen, "Star Fox", 260, BLACK, (WIDTH / 2), HEIGHT / 8)
    draw_text(screen, "Star Fox", 256, WHITE, (WIDTH / 2), HEIGHT / 8)

    draw_text(screen, "Shmup!", 260, BLACK, (WIDTH / 2), HEIGHT / 2.5)
    draw_text(screen, "Shmup!", 256, WHITE, (WIDTH / 2), HEIGHT / 2.5)

    draw_text(screen, "Press F button to start", 66, BLACK, (WIDTH / 2), (HEIGHT / 1.2))
    draw_text(screen, "Press F button to start", 64, WHITE, (WIDTH / 2), HEIGHT / 1.2)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    waiting = False


def display_game_over():
    screen.blit(background_img, background_img_rect)
    draw_text(screen, "Your score:", 128, WHITE, (WIDTH / 2), 10)
    draw_text(screen, str(player.score), 128, WHITE, (WIDTH / 2), 200)
    draw_text(screen, "You lose", 256, RED, (WIDTH / 2), 350)
    draw_text(screen, "Press F button to restart", 64, WHITE, (WIDTH / 2), HEIGHT / 1.2)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    player.lives = 3
                    player.score_multiplier = 1
                    player.shield = 100
                    player.score = 0
                    waiting = False


def generate_villans(respawn):
    amount = respawn
    now = pygame.time.get_ticks()

    # if 20 seconds have passed, add more enemys
    if (now - last_update["more_villans"]) >= 20_000:
        last_update["more_villans"] = now
        if amount < 20:
            amount += 2
        else:
            amount = 10
    # for ever enemy to spawn...
    while amount != 0:
        # ...generate a random number between 0.0 and 1.0 and safe it
        selector = random()

        # 80% chance to spawn Meteor()
        if selector <= 0.8:
            i = Meteor()
            all_sprites.add(i)
            meteors.add(i)
            amount -= 1

        # 20% chance to spawn Enemy()
        if selector > 0.8:
            i = Enemy()
            all_sprites.add(i)
            enemys.add(i)
            amount -= 1

    # if done
    return amount


def draw_the_rest():
    # GS.screen.fill(GS.BLACK)
    screen.blit(background_img, background_img_rect)
    all_sprites.draw(screen)

    # draw / render game interface
    # needs to be drawn last, to stay on top layer
    # draw_lives(surface, x, y, lives, img)
    draw_lives(screen, WIDTH / 2, 5, player.lives, player_live_img)
    # draw the players hp bar
    draw_shield_bar(screen, WIDTH - 210, 10, player.shield)
    # draw score surface
    draw_score()
    # draw the multiplier of the player
    draw_multi()
    # draw_text(surface, text, size, x, y)


def collision_check():
    # set variable to store amount of "new-spawners"
    respawn = 0

    # player hit by others
    # collision player by meteors
    hits = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    # player loses 1 life, also the hurt_mode is set to false to advoid the impact death
    for hit in hits:
        # create explosion image
        explosion = Explosion(hit.rect.center, "lg")
        all_sprites.add(explosion)

        # hurt the player
        player.hurt()

        # if meteor dies through hit, raise respawn variable
        respawn += 1

    # collision player by enemy
    hits = pygame.sprite.spritecollide(player, enemys, True, pygame.sprite.collide_circle)
    # player loses 1 life, also the hurt_mode is set to false to advoid the impact death
    for hit in hits:
        # create explosion image
        explosion = Explosion(hit.rect.center, "lg")
        all_sprites.add(explosion)

        # hurt the player
        player.hurt()

        # if enemy dies through hit, raise respawn variable
        respawn += 1

    # collision player by enemy_bullets
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    # remove player HP if hit
    for hit in hits:
        # create explosion image
        explosion = Explosion(hit.rect.center, "sm")
        all_sprites.add(explosion)

        # hurt the player
        player.hurt()

    # collision meteor by bullets
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    # if meteor dies through hit, raise respawn variable
    for hit in hits:
        # create explosion image and play its sound
        explosion = Explosion(hit.rect.center, "lg")
        all_sprites.add(explosion)
        explosion_sound.play()

        # calculate new player score
        player.score += (100 - hit.radius) * player.score_multiplier
        respawn += 1
        # 5% chance to drop power up by meteor kill
        if random() >= 0.95:
            pow = Power_Ups(hit.rect.center[0], hit.rect.center[1])
            all_sprites.add(pow)
            power_ups.add(pow)

    # collision enemys by bullets
    hits = pygame.sprite.groupcollide(enemys, bullets, True, True)
    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        # create explosion image and play its sound
        explosion = Explosion(hit.rect.center, "lg")
        all_sprites.add(explosion)
        explosion_sound.play()

        # calculate new player score
        player.score += 100 * player.score_multiplier
        respawn += 1
        # 5% chance to drop power up by enemy kill
        if random() > 0.95:
            pow = Power_Ups(hit.rect.center[0], hit.rect.center[1])
            all_sprites.add(pow)
            power_ups.add(pow)

    # collision player by power up
    hits = pygame.sprite.groupcollide(power_ups, players, True, False)
    for hit in hits:
        # enhence the quantity of players lasers
        if hit.type == "wings":
            power_up_sound["wings"].play()
            player.power_level += 1
        # raise the multiplicator score of the player
        if hit.type == "double":
            power_up_sound["double"].play()
            player.score_multiplier += 1
        # heal player for a little bit
        if hit.type == "silver":
            power_up_sound["rings"].play()
            player.shield += 15
            # check if players life raised above 100 and correct it
            if player.shield > 100:
                player.shield = 100
        # heal player for a big amount
        if hit.type == "gold":
            power_up_sound["rings"].play()
            player.shield += 50
            # check if players life raised above 100 and correct it
            if player.shield > 100:
                player.shield = 100

    return respawn
