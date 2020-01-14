import pygame
import random
import os

from enemy import Enemy
from tower import Tower

pygame.init()

star_image = pygame.image.load(os.path.join("game_assets", "star.png"))
heart_image = pygame.image.load(os.path.join("game_assets", "heart.png"))
button_pause_image = pygame.image.load(os.path.join("game_assets", "button_pause.png"))
button_play_image = pygame.image.load(os.path.join("game_assets", "button_play.png"))

class Game:

    def __init__(self):
        self.width = 1200
        self.height = 700

        self.money = 500
        self.lives = 3
        self.level = 1

        self.enemies = []
        self.enemies.append(Enemy('tiny'))  # testing

        self.towers = []
        self.towers.append(Tower('archer_long'))  # testing

        self.running = True
        self.clock = pygame.time.Clock()

        self.paused = False

        self.selected_tower = None
        self.play_pause_rect = None

        self.screen = pygame.display.set_mode([self.width, self.height])

    def run(self):
        step = 1
        mouse_dragging = False
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # self.path.append(pygame.mouse.get_pos()) # TODO delete
                    # pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 2)
                    # print(self.path)
                    pos = pygame.mouse.get_pos()
                    if self.play_pause_rect and self.play_pause_rect.collidepoint(pos): # clicked on Play/Pause
                        self.paused = not self.paused

                    for tower in self.towers: # check if clicked on one of the towers
                        if tower.get_rect().collidepoint(pos):
                            mouse_dragging = True
                            self.selected_tower = tower
                            tower.move(pos)

                if event.type == pygame.MOUSEMOTION and mouse_dragging: # move tower
                    pos = pygame.mouse.get_pos()
                    self.selected_tower.move(pos)

                if event.type == pygame.MOUSEBUTTONUP: # end dragging
                    self.selected_tower = None
                    mouse_dragging = False

            if not self.paused:
                if step % 1000 == 0: # spawn
                    self.enemies.append(Enemy('tiny'))

                # resolve shooting
                for tower in self.towers:
                    tower.attack(self.enemies)

                to_del = []
                for enemy in self.enemies:
                    if enemy.current_health <= 0:
                        to_del.append(enemy)
                        self.money += enemy.get_value()
                self.enemies = [enemy for enemy in self.enemies if enemy not in to_del]

                self.clock.tick(30)
                step += 1

        pygame.quit()

    def draw(self):
        '''
        Draw all elements
        :return: None
        '''
        # background
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, ( self.width, self.height))
        self.screen.blit(self.bg, (0, 0))

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for tower in self.towers:
            tower.draw(self.screen)

        # draw money, lives buy menu
        self.screen.blit(pygame.transform.scale(star_image, (32, 32)), (self.width * 0.9, self.height * 0.10))
        self.screen.blit(pygame.transform.scale(heart_image, (32, 32)), (self.width * 0.9, self.height * 0.18))

        # draw play pause
        if not self.paused:
            button = button_pause_image
        else:
            button = button_play_image
        self.play_pause_rect = pygame.Rect(self.width * 0.04, self.height * 0.85, 64, 64) # TODO refactore
        self.screen.blit(pygame.transform.scale(button, (64, 64)), (self.width * 0.04, self.height * 0.85))
        pygame.display.flip()

game = Game()
game.run()