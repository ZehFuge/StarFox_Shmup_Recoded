# library import block ----------------------------------------------------------------------------------------------- #
from sys import exit
from game import *


class Game():
    def __init__(self):
        # needed to display the right loop of the game class
        self.state = "menu"

        # needs to display the right background
        # 0 = menu | >0 = levels
        self.stage = 0
        # set layer vars for right layer setting
        # starting with layer = stage 1 for instant change
        self.layer = self.stage + 1



    # startmenu of the game
    def menu(self):
        # create button objects
        play_button = GS.Buttons("play", 200, 600)

        while 1:
            # check input
            self.input_handler()

            # update by behavior, get changes and draw them
            self.update_dirty_rects()


    # check which loops need to be shown
    def state_handler(self):
        if self.state == "menu":
            self.menu()

    # checks input while in any kind of menu
    def input_handler(self):
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
        # make mouse invisible, so only the image is shown
        GS.pygame.mouse.set_visible(False)

        # safe classname for events and handling
        self.classname = "Mouse"
        # needed for redrawing
        self.dirty = 1
        # set layer for draw order
        self._layer = GS.layers[self.classname]

        # add sprite to the right groups
        GS.all_sprites.add(self)
        GS.all_mouses.add(self)

        # load image and get its rect and mask
        self.image = GS.pygame.transform.rotate(GS.player_images[0], 40) # 90° angle to the left
        self.rect = self.image.get_rect()
        self.mask = GS.pygame.mask.from_surface(self.image)

        # get mouse (x,y) and set it as the rect startposition
        self.pos_x, self.pos_y = GS.pygame.mouse.get_pos()
        # set image rect.center x and y on mouse position
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y


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
        # set image rect.center x and y on mouse position
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y


mouse = Mouse()


# main loop
if __name__ == "__main__":
# while game_running == 1:
    GS.clock.tick(GS.FPS)
    game.state_handler()

