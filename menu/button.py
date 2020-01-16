import pygame

class Button():

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 64
        self.height = 64

    def draw(self, screen):
        pass

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
