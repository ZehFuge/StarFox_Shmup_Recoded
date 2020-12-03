# library import block
from sys import exit
from game import *


# game information
FPS = 60
clock = GS.pygame.time.Clock()
game_running = 1


class Game():
    def __init__(self):
        # needed to display the right loop of the game class
        self.state = "menu"

        # needed to save the mouse position for get_mouse_pos() and make it visible at the beginning
        GS.pygame.mouse.set_visible(False)
        self.mouse_pos = GS.pygame.mouse.get_pos()
        self.mouse_pressed = 0

        # needs to display the right background
        # 0 = menu
        self.stage = 0
        # set layer vars for right layer setting
        # starting with layer = stage 1 for instant change
        self.layer = self.stage + 1



    # startmenu of the game
    def menu(self):
        # create buttons
        play_button = GS.Buttons("play", 800, 500)

        while 1:
            # update mouse position
            self.get_mouse_pos()

            # check input
            self.event_handler()

            # update by behavior, get changes and draw them
            self.update_dirty_rects()

    # check which loops need to be shown
    def state_handler(self):
        if self.state == "menu":
            self.menu()

    # update mouse position
    def get_mouse_pos(self):
        self.mouse_pos = GS.pygame.mouse.get_pos()

    # checks input while in any kind of menu
    def event_handler(self):
        for event in GS.pygame.event.get():
            if event.type == GS.pygame.QUIT:
                self.end_game()

            if event.type == GS.pygame.mouse.get_pressed():
                self.mouse_pressed = GS.pygame.mouse.get_pressed()

    # if event.type == QUIT
    def end_game(self):
        GS.pygame.quit()
        exit()


    # update by behavior, get changes and draw them
    def update_dirty_rects(self):
        GS.all_sprites.update()
        rects = GS.all_sprites.draw(GS.screen)
        GS.pygame.display.update(rects)
        GS.pygame.display.flip()

    # change the background depend on self.stage re-rendering
    def change_background_clear(self):
        GS.all_sprites.clear(GS.screen, GS.backgrounds[self.stage])


# create game object before mouse object
# makes it possible to be manipulated by mouse object
game = Game()


class Mouse(GS.pygame.sprite.DirtySprite):
    def __init__(self):
        GS.pygame.sprite.DirtySprite.__init__(self)
        # safe classname for events and handling
        self.classname = "Mouse"
        # needed for redrawing
        self.dirty = 1
        # set layer for draw order
        self._layer = GS.layers[self.classname]

        GS.all_sprites.add(self)
        GS.all_mouses.add(self)

        # load image and get its rect and mask
        self.image = GS.pygame.transform.rotate(GS.player_images[0], 40) # 90° angle to the left
        self.rect = self.image.get_rect()
        self.mask = GS.pygame.mask.from_surface(self.image)

        # set radius for clearner collision detection with buttons

        # get mouse (x,y) and set it as the rect startposition
        self.pos_x, self.pos_y = GS.pygame.mouse.get_pos()
        # -5 for better positioning of the image to the mouse
        self.position_correction = -30
        self.rect.x = self.pos_x - self.position_correction
        self.rect.y = self.pos_y - self.position_correction

    # set objects behavior
    def update(self):
        # keep mask updated
        self.mask = GS.pygame.mask.from_surface(self.image)

        # get position of the mouse cursor
        self.get_position()

        # change mouse (x,y) depending on position
        self.sprite_repos()

        # always draw the mouse sprite
        self.dirty = 1

    def get_position(self):
        # safe new position
        self.pos_x, self.pos_y = GS.pygame.mouse.get_pos()

    def sprite_repos(self):
        # - 5 for better mouse positioning
        self.rect.x = self.pos_x - self.position_correction
        self.rect.y = self.pos_y - self.position_correction


mouse = Mouse()


while game_running == 1:
    clock.tick(FPS)
    game.state_handler()

