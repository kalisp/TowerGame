import pygame

import os

class Button():

    def __init__(self, img, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.width = 64
        self.height = 64

        self.img = img

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    # def get_rect(self):
    #     ''' Get bounding rectangle for checking if clicked
    #         self.x, self.y is center, rect needs to be around it, no starting from it
    #     '''
    #     return pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)

    def clicked(self, pos):
        ''' Check if mouse event on 'pos' was inside of Button area '''
        rect = pygame.Rect(self.x, self.y, self.width, self.height)  # self.x, self.y top left, not center, here

        return rect.collidepoint(pos)

class PlayPauseButton(Button):
    ''' Display Play/Pause button and check if mouse clicked '''
    def __init__(self, play_img, pause_img, pos):
        self.x, self.y = pos
        self.play_img = play_img
        self.pause_img = pause_img
        self.paused = False
        self.width = play_img.get_width()
        self.height = play_img.get_height()

    def set_paused(self, paused):
        self.paused = paused

    def draw(self, screen):
        if self.paused:  # picture depends on state of game
            img = self.pause_img
        else:
            img = self.play_img
        screen.blit(img, (self.x, self.y))

class UpgradeButton(Button):
    ''' Small button for TowerMenu '''
    def __init__(self, img, pos):
        super(UpgradeButton, self).__init__(img, pos)
        self.img = img
        self.width = img.get_width()
        self.height = img.get_height()

    def action(self, tower):
        tower.upgrade()

    def update_position(self, pos):
        self.x, self.y = pos[0], pos[1]

class DestroyButton(UpgradeButton):
    ''' Small button for TowerMenu - to sell/destroy tower'''
    def __init__(self, img, pos):
        #super.__init(img, pos)
        super(DestroyButton, self).__init__(img, pos)

    def action(self, tower):
        tower.sell()