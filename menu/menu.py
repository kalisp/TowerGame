import pygame
import os

from menu import button

upgrade_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "upgrade.png")), (32, 32))
destroy_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "destroy.png")), (32, 32))

archer_tower_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "icon_archer.png")), (64, 64))
archer_long_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "icon_long_archer.png")), (64, 64))
bolt_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "icon_bolt.png")), (64, 64))

class Menu():
    ''' Generic, abstract menu'''
    def __init__(self, pos, img):
        self.x, self.y = pos
        self.width = 64 # temporary value, will be recalculated in update_size
        self.height = 64 # temporary value, will be recalculated in update_size

        self.offset = 20
        self.padding = 10
        self.buttons = []

        self.img = img

    def update_size(self):
        '''Called after adding at least 1 Button, as size is calculated from button size'''

        self.padding = 10
        # print("type {} ".format(self.buttons[0]))
        # print("upgrade_img {} {}".format(upgrade_img.get_width(), upgrade_img.get_height()))
        # print("button {} {}".format(self.buttons[0].width, self.buttons[0].height))
        self.width = self.buttons[0].width + self.padding
        self.height = len(self.buttons) * self.buttons[0].height + self.padding
        # print("towermenu {}, {}".format(self.width, self.height))
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    def item_clicked(self, pos):
        ''' Returns button item if clicked, None otherwise '''
        for button in self.buttons:
            if button.clicked(pos):
                return button

        return None

    def draw(self, screen):
        screen.blit(self.img, (self.x + self.offset, self.y + self.offset))  # first draw background

        for index, button in enumerate(self.buttons):
            button.set_position((self.x + self.offset + ((self.width - button.width) / 2) + self.padding / 2,
                                    self.y + self.offset + (button.height * index) + self.padding / 2))
            button.draw(screen)

class TowerMenu(Menu):
    ''' Small menu triggered by RMB on tower instance
        Used for upgrading and selling instance
    '''
    def __init__(self, pos, tower, tower_menu_image):
        super(TowerMenu, self).__init__(pos)
        self.buttons.append(button.UpgradeButton(upgrade_img, (self.x + 5, self.y + 5)))
        self.buttons.append(button.DestroyButton(destroy_img, (self.x + 5, self.y + 5)))

        self.img = tower_menu_image

        self.update_size()

    def draw(self, screen):
        ''' Draws tower menu.
            Modifies x, y position if menu wouldn't fit into screen.
        '''
        if self.x + self.offset + self.width > screen.get_width():  # overflowing from screen
            self.x -= self.tower.width + self.width

        if self.y + self.offset + self.height > screen.get_height():
            self.y -= self.tower.height + self.height

        super.draw(screen)


class NewTowersMenu(Menu):
    ''' Right hand side menu for adding new towers'''
    def __init__(self, pos, bg_img):
        super(NewTowersMenu, self).__init__(pos, bg_img)
        print("NewTowersMenu {}".format(pos))
        self.buttons.append(button.AddArcherTowerButton(archer_tower_img, (self.x + 5, self.y + 5)))
        self.buttons.append(button.AddArcherLongTowerButton(archer_long_img, (self.x + 5, self.y + 5)))
        self.buttons.append(button.AddBoltTowerButton(bolt_img, (self.x + 5, self.y + 5)))

        self.offset = 0 # no need to have offset from position

        self.update_size()

