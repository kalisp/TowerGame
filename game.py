import pygame
import random
import os

from enemy import Enemy
from tower import Tower
from menu import button
from menu import menu

pygame.init()
pygame.font.init()



star_image = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "star.png")), (32, 32))
heart_image = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "heart.png")), (32, 32))
button_pause_image = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "button_pause.png")), (64, 64))
button_play_image = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "button_play.png")), (64, 64))

# n arrays, where each item denotes count of enemies of specific type
# type of enemies:
waves = [
    [5, 0, 0, 0],
    [10, 0, 0, 0]
]

class Game:

    def __init__(self):
        self.width = 1200
        self.height = 700

        self.money = 500
        self.lives = 3
        self.wave_number = 0 # number of currently running wave

        self.enemies = []
        self.enemies.append(Enemy('tiny'))  # testing

        self.towers = []
        self.towers.append(Tower('archer_long'))  # testing

        self.running = True
        self.clock = pygame.time.Clock()

        self.paused = False

        self.selected_tower = None
        self.play_pause_rect = None
        
        self.spawn_x_ticks = 30 # TODO extend by levels (easy, standard, hard)

        self.screen = pygame.display.set_mode([self.width, self.height])
        self.life_font = pygame.font.SysFont("comicsans", 50)

        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "bg.png")),
                                         (self.width, self.height))

        self.current_wave_enemies = waves[0]
        self.enemies_types = ['tiny', 'tiny', 'tiny', 'tiny']

        self.playButton = button.PlayPauseButton(button_play_image, button_pause_image, (self.width * 0.04, self.height * 0.85))
        self.tower_menu = None  # to display menu on RMB on Tower

    def run(self):
        tick = 1
        more_enemies = False
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

                    if self.playButton.clicked(pos):  # clicked on Play/Pause
                        self.paused = not self.paused

                    if event.button == pygame.BUTTON_RIGHT: # RMB deletes existing TowerMenu from everywhere
                        if self.tower_menu:
                            self.tower_menu = None

                    for tower in self.towers: # check if clicked on one of the towers
                        if tower.clicked(pos):
                            self.selected_tower = tower
                            if event.button == pygame.BUTTON_LEFT:
                                mouse_dragging = True

                            if event.button == pygame.BUTTON_RIGHT:
                                # not sure if this should be here at all, if shouldnt be handled by Tower.draw
                                if not self.tower_menu:
                                    self.tower_menu = menu.TowerMenu(pos, tower)

                if event.type == pygame.MOUSEMOTION and mouse_dragging and self.paused: # move tower only if paused
                    pos = pygame.mouse.get_pos()
                    self.selected_tower.move(pos)

                if event.type == pygame.MOUSEBUTTONUP: # end dragging
                    self.selected_tower = None
                    mouse_dragging = False

            if not self.paused:
                if tick % self.spawn_x_ticks == 0: # spawn
                    if sum(self.current_wave_enemies) > 0:
                        moreEnemies = True
                        for i in range(len(self.current_wave_enemies)):
                            if self.current_wave_enemies[i] > 0:
                                self.enemies.append(Enemy(self.enemies_types[i]))
                                self.current_wave_enemies[i] -= 1
                                break
                    else:
                        moreEnemies = False
                        self.wave_number = (self.wave_number + 1) % len(waves) # TODO add end of game
                        self.current_wave_enemies = waves[self.wave_number]

                # resolve shooting
                for tower in self.towers:
                    tower.attack(self.enemies)

                to_del = []
                for enemy in self.enemies:
                    if enemy.current_health <= 0:
                        to_del.append(enemy)
                        self.money += enemy.get_value()
                    elif enemy.x <= 0 and not enemy.moving_right:
                        # expecting that enemies always leave scene from right to left
                        # they could have negative x when they are entering scene
                        to_del.append(enemy)
                        self.lives -= 1
                    else:
                        enemy.move()
                self.enemies = [enemy for enemy in self.enemies if enemy not in to_del]

                if self.enemies == [] and not moreEnemies:
                    # last enemy in the wave killed, stop game
                    self.paused = True
                    
                self.clock.tick(30)
                tick += 1

        pygame.quit()

    def draw(self):
        '''
        Draw all elements
        :return: None
        '''
        # background
        self.screen.blit(self.bg, (0, 0))

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for tower in self.towers:
            tower.draw(self.screen)

        # draw money, lives buy menu
        self.screen.blit(star_image, (self.width * 0.9, self.height * 0.10))
        self.screen.blit(self.life_font.render(str(self.money), False, pygame.Color('red')), (self.width * 0.94, self.height * 0.11))
        self.screen.blit(heart_image, (self.width * 0.9, self.height * 0.18))
        self.screen.blit(self.life_font.render(str(self.lives), False, pygame.Color('red')), (self.width * 0.94, self.height * 0.18))

        # draw play pause
        self.playButton.set_paused(self.paused)
        self.playButton.draw(self.screen)

        # draw tower menu
        if self.tower_menu:
            self.tower_menu.draw(self.screen)

        pygame.display.flip()

game = Game()
game.run()