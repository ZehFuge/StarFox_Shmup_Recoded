# library import block ----------------------------------------------------------------------------------------------- #
from os import path
import pygame


# library init block ------------------------------------------------------------------------------------------------- #
pygame.init
pygame.mixer.pre_init(44100, -16, 50, 4096)
pygame.mixer.init()
pygame.font.init()

# predefined colors - delete later if transparencys are made
RED = (255, 0, 0)

# window information ------------------------------------------------------------------------------------------------- #
WIDTH = 1200
HIGHT = 800
screen = pygame.display.set_mode((WIDTH, HIGHT))
FPS = 60
clock = pygame.time.Clock()
# save game draw time for FPS independet drawing
game_dt = clock.tick(FPS) / 1000


# saving paths ------------------------------------------------------------------------------------------------------- #
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


# image loading block ------------------------------------------------------------------------------------------------ #
# load backgrounds
backgrounds = { 0: pygame.image.load(path.join(img_dir, "background_menu_1200x800.png")).convert(),
                1: pygame.image.load(path.join(img_dir, "background_space_1200x800.png")).convert()}

# load buttons
# 0 = idle | 1 = mouseover
buttons = {"play0" : pygame.image.load(path.join(img_dir, "button_play.png")).convert_alpha(),
           "play1" : pygame.image.load(path.join(img_dir, "button_play_mouseover.png")).convert_alpha(),
           "howto0": pygame.image.load(path.join(img_dir, "button_howto.png")).convert_alpha(),
           "howto1": pygame.image.load(path.join(img_dir, "button_howto_mouseover.png")).convert_alpha(),
           "menu0" : pygame.image.load(path.join(img_dir, "button_menu.png")).convert_alpha(),
           "menu1" : pygame.image.load(path.join(img_dir, "button_menu_mouseover.png")).convert_alpha(),
           "next0" : pygame.image.load(path.join(img_dir, "button_next.png")).convert_alpha(),
           "next1" : pygame.image.load(path.join(img_dir, "button_next_mouseover.png")).convert_alpha(),
           "exit0" : pygame.image.load(path.join(img_dir, "button_exit.png")).convert_alpha(),
           "exit1" : pygame.image.load(path.join(img_dir, "button_exit_mouseover.png")).convert_alpha()}


# load information/menu images
info_images = {"howto0" : pygame.image.load(path.join(img_dir, "info_movement.png")).convert(),
            "howto1" : pygame.image.load(path.join(img_dir, "info_powerups.png")).convert()}

# set colorkey | remove after images are made transparent
info_images["howto0"].set_colorkey(RED)
info_images["howto1"].set_colorkey(RED)
buttons["next0"].set_colorkey(RED)
buttons["next1"].set_colorkey(RED)


# load player sprites
player_images = {0: pygame.image.load(path.join(img_dir, "arwing_idle.png")).convert_alpha(),
                 1: pygame.image.load(path.join(img_dir, "arwing_left.png")).convert_alpha(),
                 2: pygame.image.load(path.join(img_dir, "arwing_right.png")).convert_alpha()}

# transform player sprites to right size
# ...until I get my shit done making it in the right size as png
for counter in player_images:
    player_images[counter] = pygame.transform.scale(player_images[counter], (96, 96))


# create groups ------------------------------------------------------------------------------------------------------ #
all_buttons = pygame.sprite.Group()
all_mouses = pygame.sprite.Group()
all_infos = pygame.sprite.Group()
all_players = pygame.sprite.Group()

# create the all sprites group from here, to use all classes
all_sprites = pygame.sprite.LayeredDirty()


# layer predefinition block ------------------------------------------------------------------------------------------ #
# create layer for an object
#   self._layer = layers[classname]
layers = {"background_fx": 1,
          "Info_Images"  : 2,
          "Buttons"      : 3,
          "Mouse"        : 4,
          "Player"       : 5,
          "Enemy"        : 5,
          "Meteor"       : 6,
          "GUI"          : 7}


# sound loading block ------------------------------------------------------------------------------------------------ #
sounds = {"Buttons": pygame.mixer.Sound(path.join(snd_dir, "menu_mouseover_sfx.ogg"))}


# sound volume block ------------------------------------------------------------------------------------------------- #
sounds["Buttons"].set_volume(0.5)


# game handling classes block ---------------------------------------------------------------------------------------- #
# used to create buttons
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

        # set idle button image at first and get its rectangle
        self.buttontype = buttontype

        # set vars for collision handling
        self.collision = 0
        self.collision_detector = 0

        # load image and get its rect and mask
        self.image = buttons[self.buttontype + str(self.collision)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # set rectangle to given position
        self.rect.x = x
        self.rect.y = y

    # ---------------------------------------------------------------------------------------------------------------- #
    def update(self):
        # check for collision
        self.check_collision()

    # change self.image depending on collision ----------------------------------------------------------------------- #
    # also used to play mouseover sound
    def change_image(self, hits):
        # if there is a collision ...
        if hits:
            # ... check if image is already changed
            if self.image != buttons[self.buttontype + str(1)]:
                # if not, change it and set dirty
                self.image = buttons[self.buttontype + str(1)]
                sounds[self.classname].play()
                self.dirty = 1
        # if there is no collision
        else:
            # ... check if image is already changed
            if self.image != buttons[self.buttontype + str(0)]:
                # if not, change it and set dirty
                self.image = buttons[self.buttontype + str(0)]
                self.dirty = 1

    # ---------------------------------------------------------------------------------------------------------------- #
    def check_collision(self):
        # check if sprite rects collide
        hits = pygame.sprite.spritecollideany(self, all_mouses)

        # if True, start a pixel perfect collision detection
        if hits:
            mask_hits = pygame.sprite.spritecollideany(self, all_mouses, pygame.sprite.collide_mask)
        else:
            mask_hits = None

        # set image changes if needed
        self.change_image(mask_hits)


# used to show info images like controls and handle them ------------------------------------------------------------- #
class Info_Images(pygame.sprite.DirtySprite):
    def __init__(self, gamestate, toggle, x, y):
        pygame.sprite.DirtySprite.__init__(self)

        # safe classname for events and handling
        self.classname = "Info_Images"

        # needed for redrawing
        self.dirty = 1

        # set layer for draw order
        self._layer = layers[self.classname]

        # add to group after setting layer
        all_sprites.add(self)
        all_infos.add(self)

        # save given toggle options
        self.toggle = toggle
        self.old_toggle = toggle

        # load image and get its rect and mask
        self.gamestate = gamestate
        self.image = info_images[self.gamestate + str(self.toggle)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # set sprite behavior -------------------------------------------------------------------------------------------- #
    def update(self):
        # check which page should be shown (if user presses "next" button)
        self.check_toggle()

        # always draw
        self.dirty = 1

    # handling toggling by "next" button ----------------------------------------------------------------------------- #
    def check_toggle(self):
        if self.toggle != self.old_toggle:
            self.image = info_images[self.gamestate + str(self.toggle)]
            self.old_toggle = self.toggle


# sprite classes block ----------------------------------------------------------------------------------------------- #
class Player(pygame.sprite.DirtySprite):
    def __init__(self, x, y):
        pygame.sprite.DirtySprite.__init__(self)

        # safe classname for events and handling
        self.classname = "Player"

        # needed for redrawing
        self.dirty = 1

        # set layer for draw order
        self._layer = layers[self.classname]

        # add to group after setting layer
        all_sprites.add(self)
        all_players.add(self)

        # set var for movestatement
        # 0 = idle | 1 = left | 2 = right
        self.fly_direction = 0

        # set image for object and get its rect and mask
        self.image = player_images[self.fly_direction]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # get start position
        self.rect.x = x
        self.rect.y = y

        # declare movement speed of object
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity = 150


    def update(self):
        # check input for movement update
        self.movement_handler()


    # get keyboard input and change position ------------------------------------------------------------------------- #
    def movement_handler(self):
        # reset movespeed
        # self.velocity_x = 0
        # self.velocity_y = 0

        keystate = pygame.key.get_pressed()

        # check if player moved (W, A, S, D)
        if keystate[pygame.K_w]:
            self.velocity_y = -self.velocity
        if keystate[pygame.K_a]:
            self.velocity_x = -self.velocity
            self.fly_direction = 1
        if keystate[pygame.K_s]:
            self.velocity_y = self.velocity
        if keystate[pygame.K_d]:
            self.velocity_x = self.velocity
            self.fly_direction = 2

        if not keystate[pygame.K_w] and not keystate[pygame.K_s]:
            self.velocity_y = 0
        if not keystate[pygame.K_a] and not keystate[pygame.K_d]:
            self.velocity_x = 0

        # reset fly direction if player isn't moving left (1) or right (2) back to idle (0)
        if not keystate[pygame.K_a] and not keystate[pygame.K_d]:
            self.fly_direction = 0
            self.dirty = 1

        # change image depending on self.fly_direction
        self.set_move_image()

        # handle diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *=  0.9
            self.velocity_y *= 0.9


        """ # move sprite -------------------------------------------------------------------------------------------- #
        #
        #                                                Usage notes:
        #
        # The movement speed needs to be converted to an integer. If not, the movement speed to
        # the left will be faster then moving to the right. Afte a conversion, the speed will remain the same
        # for all directions.
        # ------------------------------------------------------------------------------------------------------------ #
        """
        # Test for sprite movement ----------------------------------------------------------------------------------- #
        # print("vel x: {},"
        #       "vel y: {}".format(self.velocity_x, self.velocity_y))

        self.rect.centerx += int(self.velocity_x * game_dt)
        self.rect.centery += int(self.velocity_y * game_dt)

        # check if player wants to leave the screen
        self.check_moverange()

        # update image
        self.dirty = 1

    # stops player to leave screen ----------------------------------------------------------------------------------- #
    def check_moverange(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HIGHT:
            self.rect.bottom = HIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    # update image by move_image counter and get new mask ------------------------------------------------------------ #
    def set_move_image(self):
        self.image = player_images[self.fly_direction]
        self.mask = pygame.mask.from_surface(self.image)

# test environment --------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    pass
