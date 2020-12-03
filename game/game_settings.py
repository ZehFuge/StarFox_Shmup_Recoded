# library import block
from os import path
from random import randrange
from random import choice
from random import randint
from random import random
import pygame


# library init block
pygame.init
# pygame.mixer.pre_init(44100, -16, 50, 4096)
# pygame.mixer.init()
# pygame.font.init()


# window information
WIDTH = 1200
HIGHT = 800
screen = pygame.display.set_mode((WIDTH, HIGHT))


# pre defined colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CONVERT_SCORE = (89, 193, 53)
CONVERT_WINGS = (172, 50, 50)
CONVERT_PLAYER = (181, 230, 29)


# save image and sound folder dir to var
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


# image loading block
# load backgrounds
backgrounds = {}
backgrounds[0] = pygame.image.load(path.join(img_dir, "space_background_1200x800_nsm.png")).convert()

# load buttons
# 0 = idle | 1 = mouseover
buttons = {}
buttons["play0"] = pygame.image.load(path.join(img_dir, "startmenu_play_button_rgb_red.png")).convert()
buttons["play1"] = pygame.image.load(path.join(img_dir, "startmenu_play_button_mouseover_rgb_red.png")).convert()

# buttons set colorkey
buttons["play0"].set_colorkey(RED)
buttons["play1"].set_colorkey(RED)

# load player sprites
player_images = {}
player_images[0] = pygame.image.load(path.join(img_dir, "arwing_idle.png")).convert_alpha()
player_images[1] = pygame.image.load(path.join(img_dir, "arwing_left.png")).convert_alpha()
player_images[2] = pygame.image.load(path.join(img_dir, "arwing_right.png")).convert_alpha()

# transform player sprites to right size
# ...until I get my shit done making it in the right size as png
for counter in range(3):
    player_images[counter] = pygame.transform.scale(player_images[counter], (96, 96))


# create groups
all_buttons = pygame.sprite.Group()
all_mouses = pygame.sprite.Group()

# create the all sprites group from here, to use all classes
all_sprites = pygame.sprite.LayeredDirty()
# set first clear image and the surface
all_sprites.clear(screen, backgrounds[0])


# layer predefinition block
# create layer for an object
#   self._layer = layers[classname]
layers = {}
layers["Buttons"] = 1
layers["Mouse"] = 2


# class block
# creates a
class Buttons(pygame.sprite.DirtySprite):
    def __init__(self, buttontype, x, y):
        # asign sprite to groups
        pygame.sprite.DirtySprite.__init__(self)
        # safe classname for events and handling
        self.classname = "Buttons"
        # needed for redrawing
        self.dirty = 1
        # set layer for draw order
        self._layer = layers[self.classname]

        # add to group after setting layer
        all_sprites.add(self)
        all_buttons.add(self)

        # needed to change between idle and mouseover button
        self.image_counter = 0

        # set idle button image at first and get its rectangle
        self.buttontype = buttontype
        self.image = buttons[self.buttontype + str(self.image_counter)]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2

        # set rectangle to given position
        self.rect.x = x
        self.rect.y = y

        # let sounds only play once
        self.soundcontroller = 1

    def update(self):
        # check collision
        self.check_collision()

        # change image if needed
        self.change_image()

    def check_collision(self):
        hits = pygame.sprite.spritecollide(self, all_mouses, False)

        if hits:
            if self.image_counter == 0:
                self.image_counter = 1
                self.dirty = 1
        else:
            if self.image_counter == 1:
                self.image_counter = 0
                self.dirty = 1

    def change_image(self):
        self.image = buttons[self.buttontype + str(self.image_counter)]
