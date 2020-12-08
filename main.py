# library import block ----------------------------------------------------------------------------------------------- #
from sys import exit
from game import *


# define game handling ----------------------------------------------------------------------------------------------- #
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

        # create group for generated buttons objects
        self.shown_buttons = {}

        # used to toggle shown menu screens
        # toggle needs always to be resetted to 0, except if another page should be shown
        self.toggle = 0
        self.old_toggle = self.toggle

        # left click is saved here and not in the mouse class because of latency in input
        self.left_click = 0


    # startmenu of the game ------------------------------------------------------------------------------------------ #
    def menu(self):
        # set clear image and the surface
        self.change_background_clear()

        # create button objects in screen order
        play_button = GS.Buttons("play", 50, 600)
        howto_button = GS.Buttons("howto", 450, 600)
        exit_button = GS.Buttons("exit", 850, 600)

        # save buttons in a list for easier kill and create
        # buttons get killed in mouse method mouse.check_collision
        shown_buttons = {play_button, howto_button, exit_button}

        # handle menu until state gets changed by mouse.check_buttonpress while button collision
        while self.state == "menu":
            # check input
            self.input_handler()

            # update by behavior, get changes and draw them
            self.update_dirty_rects()

        # if loop ends, kill created objects
        for button in shown_buttons:
            button.kill()


    # loop of the actual game ---------------------------------------------------------------------------------------- #
    def play(self):
        # set clear image and the surface
        self.change_background_clear()

        # create player object
        player = GS.Player(GS.WIDTH / 2, 700)

        while self.state == "play":
            # check input
            self.input_handler()

            # update by behavior, get changes and draw them
            self.update_dirty_rects()


    # handle how until state gets changed by mouse.check_buttonpress while button collision -------------------------- #
    def howto(self):
        # set clear image and the surface
        self.change_background_clear()

        # set toggle to 0 before loop to avoid errors in runtime
        self.toggle = 0

        # create button objects in screen order
        menu_button = GS.Buttons("menu", 300, 670)
        next_button = GS.Buttons("next", 650, 670)

        # save buttons in a list for easier kill and create
        # buttons get killed in mouse method mouse.check_collision
        shown_buttons = {menu_button, next_button}

        # create info menu object
        info_object = GS.Info_Images(self.state, self.toggle, 255, 50)

        while self.state == "howto":
            # check if info_objects toggle needs to be changed
            if self.old_toggle != self.toggle:
                info_object.toggle = self.toggle
                self.old_toggle = self.toggle

            # check input
            self.input_handler()

            # update all_sprites by behavior, get changes and draw them
            self.update_dirty_rects()

        # if loop ends, kill created objects
        for button in shown_buttons:
            button.kill()
        info_object.kill()

    # check which loops need to be shown ----------------------------------------------------------------------------- #
    def state_handler(self):
        # main menu
        if self.state == "menu":
            self.stage = 0
            self.menu()

        # actual game loop
        if self.state == "play":
            self.stage = 1
            self.play()

        # show instructions
        if self.state == "howto":
            self.howto()


        # end game if exit was clicked
        if self.state == "exit":
            self.end_game()

    # checks input while in any kind of menu ------------------------------------------------------------------------- #
    def input_handler(self):
        for event in GS.pygame.event.get():
            # quit game input ---------------------------------------------------------------------------------------- #
            if event.type == GS.pygame.QUIT:
                self.end_game()


            # keyboard inputs ---------------------------------------------------------------------------------------- #
            if event.type == GS.pygame.KEYDOWN:
                # no keydown events at the moment
                pass


            # mouse inputs ------------------------------------------------------------------------------------------- #
            if event.type == GS.pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = 1
            if event.type == GS.pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_click = 0


    # if event.type == QUIT ------------------------------------------------------------------------------------------ #
    def end_game(self):
        GS.pygame.quit()
        exit()


    # update by behavior, get changes and draw them ------------------------------------------------------------------ #
    def update_dirty_rects(self):
        GS.all_sprites.update()
        rects = GS.all_sprites.draw(GS.screen)
        GS.pygame.display.update(rects)
        GS.pygame.display.flip()

    # change the background depend on self.stage re-rendering -------------------------------------------------------- #
    def change_background_clear(self):
        # set new clear picture
        GS.all_sprites.clear(GS.screen, GS.backgrounds[self.stage])

        # draw new background screen to erase old one
        GS.screen.blit(GS.backgrounds[self.stage], (0, 0))


# create game object before mouse object
# makes it possible to be manipulated by mouse object
game = Game()


# define mouse handling ---------------------------------------------------------------------------------------------- #
class Mouse(GS.pygame.sprite.DirtySprite):
    def __init__(self):
        GS.pygame.sprite.DirtySprite.__init__(self)

        """
        # ------------------------------------------------------------------------------------------------------------ #
        #                                                Usage notes:
        #
        # LEFT CLICK FROM MOUSE IS TAKE IN GAME CLASS:
        # Left mouse button input is saved in the game class because of the lack of input check speed. In this class,
        # every 20th-30th mouse click would have been taken.
        # ------------------------------------------------------------------------------------------------------------ #
        """

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


    # set objects behavior ------------------------------------------------------------------------------------------- #
    def update(self):
        self.handle_visibility()
        # get position of the mouse cursor
        self.get_position()

        # check collision to change game.state
        self.check_collision()

        # change mouse (x,y) depending on position
        self.sprite_repos()

        # always draw the mouse sprite
        self.dirty = 1

    # ---------------------------------------------------------------------------------------------------------------- #
    def get_position(self):
        # safe new position
        self.pos_x, self.pos_y = GS.pygame.mouse.get_pos()

    # ---------------------------------------------------------------------------------------------------------------- #
    def sprite_repos(self):
        # set image rect.center x and y on mouse position
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

    # ---------------------------------------------------------------------------------------------------------------- #
    def check_collision(self):
        # check if sprite rects collide
        hits = GS.pygame.sprite.spritecollideany(self, GS.all_buttons)

        # if True, start a pixel perfect collision detection
        if hits:
            mask_hits = GS.pygame.sprite.spritecollideany(self, GS.all_buttons, GS.pygame.sprite.collide_mask)

            # check if left click is done by user
            if mask_hits and game.left_click == 1:
                # check button isn't a "next" button, change game.state
                if mask_hits.buttontype != "next":
                    # reset left click to be only taken once
                    game.left_click = 0

                if mask_hits.buttontype != "next":
                    # change game.state depending on the button
                    game.state = mask_hits.buttontype
                    # reset left click to be only taken once
                    game.left_click = 0
                # otherwise just rais the game.toggle (if buttontype == "next")
                else:
                    # reset left click to be only taken once
                    game.left_click = 0
                    # show next or previous info page
                    if game.toggle == 0:
                        game.toggle = 1
                    else:
                        game.toggle = 0
        else:
            mask_hits = None

    # set mouse visibility depending on game.state ------------------------------------------------------------------- #
    def handle_visibility(self):
        # check if games started and mouse images needs to be removed
        if game.state == "play":
            # check if there is a mouse object in the GS.all_sprites group
            # lets methode run only once
            if self in GS.all_sprites:
                # if all conditions are true, remove mouse object (self) from draw group (GS.all_sprites)
                GS.all_sprites.remove(self)

        # check if play is in any kind of menu
        if game.state != "play":
            # check if mouse object already is in a group
            # lets methode run only once
            if not self in GS.all_sprites:
                # if all conditions are true, add mouse object (self) from draw group (GS.all_sprites)
                GS.all_sprites.add(self)

# create mouse object before the main loop
mouse = Mouse()


# main loop ---------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    while game:
        GS.clock.tick(GS.FPS)
        game.state_handler()
