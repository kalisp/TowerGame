import pygame
import os

tower_menu_image = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "table.png")), (64, 64))

class TowerMenu():

    def __init__(self, pos, tower):
        self.width = 100
        self.height = 100 # ??
        self.x, self.y = pos[0], pos[1] # mouse position
        self.offset = 20

    def draw(self, screen):
        ''' Draws tower menu.
            Modifies x, y position if menu wouldn't fit into screen.
        '''
        if self.x + self.offset + self.width > screen.get_width():  # overflowing from screen
            self.x -= self.tower.width + self.width

        if self.y + self.offset + self.height > screen.get_height():
            self.y -= self.tower.height + self.height

        # surface = pygame.Surface((self.width, self.height))
        # surface.fill(pygame.Color("gray"))
        screen.blit(tower_menu_image, (self.x + self.offset, self.y + self.offset))

