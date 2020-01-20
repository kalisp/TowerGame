import pygame
import os

from menu import button

upgrade_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "upgrade.png")), (32, 32))
destroy_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu",  "destroy.png")), (32, 32))

class TowerMenu():
    ''' Small menu triggered by RMB on tower instance
        Used for upgrading and selling instance
    '''
    def __init__(self, pos, tower, tower_menu_image):
        self.x, self.y = pos[0], pos[1] # mouse position
        self.offset = 20
        self.buttons = []
        self.buttons.append(button.UpgradeButton(upgrade_img, (self.x + 5, self.y + 5)))
        self.buttons.append(button.DestroyButton(destroy_img, (self.x + 5, self.y + 5)))

        self.padding = 10
        print("type {} ".format(self.buttons[0]))
        print("upgrade_img {} {}".format(upgrade_img.get_width(), upgrade_img.get_height()))
        print("button {} {}".format(self.buttons[0].width, self.buttons[0].height))
        self.width = self.buttons[0].width + self.padding
        self.height = len(self.buttons) * self.buttons[0].height + self.padding
        print("towermenu {}, {}".format(self.width, self.height))
        self.img = pygame.transform.scale(tower_menu_image, (self.width, self.height))

    def item_clicked(self, pos):
        ''' Returns button item if clicked, None otherwise '''
        for button in self.buttons:
            if button.clicked(pos):
                return button

        return None

    def draw(self, screen):
        ''' Draws tower menu.
            Modifies x, y position if menu wouldn't fit into screen.
        '''
        if self.x + self.offset + self.width > screen.get_width():  # overflowing from screen
            self.x -= self.tower.width + self.width

        if self.y + self.offset + self.height > screen.get_height():
            self.y -= self.tower.height + self.height

        screen.blit(self.img, (self.x + self.offset, self.y + self.offset))  # first draw background

        for index, button in enumerate(self.buttons):
            button.update_position((self.x + self.offset + ((self.width - button.width) / 2) + self.padding / 2,
                                    self.y + self.offset + (button.height * index) + self.padding / 2))
            button.draw(screen)



