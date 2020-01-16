import pygame

import os

class Enemy(pygame.sprite.Sprite):
    '''
    Abstract class for enemy.
    Moves, draws enemy
    '''
    STEP = 5
    def __init__(self, name):
        super(Enemy, self).__init__()
        self.name = name
        self.max_health = 20
        self.current_health = self.max_health
        self.value = 20

        self.x = -100
        self.y = 228
        self.height = 64
        self.width = 64
        self.animation_step = 0
        self.path_position = 0  # initial path position
        self.path = [(5, 228), (174, 229), (253, 280), (555, 276), (616, 204), (666, 70), (788, 69), (871, 260),
                     (1020, 317), (1046, 440), (984, 501), (725, 516), (666, 559), (141, 552), (90, 475), (66, 383),
                     (3, 339), (-100, 339)]

        self.surface = pygame.Surface((self.width, self.height))
        self.images = self.prepare_images()
        self.moving_right = True


    def draw(self, screen):
        ''' Draws surface '''
        #self.surface.fill((50, 50, 50))
        url = self.images[self.animation_step]
        image = pygame.image.load(url)
        if not self.moving_right:
            image = pygame.transform.flip(image, True, False)
        screen.blit(pygame.transform.scale(image, (self.width, self.height)),
                                                                   (self.x - self.width / 2 , self.y - self.height / 2))

        max_health_rect = pygame.Rect(self.x - 44, self.y - 32, self.width, 4)
        pygame.draw.rect(screen, pygame.Color('red'), max_health_rect)

        current_health = pygame.Rect(self.x - 44, self.y - 32, self.width * self.current_health / self.max_health , 4)
        pygame.draw.rect(screen, pygame.Color('green'), current_health)

    def move(self):
        ''' Calls move, triggered only if game is not paused'''
        if self.path_position < len(self.path):
            speed = 5
            current_pos = pygame.math.Vector2(self.x, self.y)
            next_pos = self.path[self.path_position]
            next_pos_vector = pygame.math.Vector2(next_pos)
            if next_pos_vector.distance_to(current_pos) <= speed:
                self.path_position += 1
                if self.path_position < len(self.path): # returned out of picture
                    next_pos_vector = pygame.math.Vector2(self.path[self.path_position])
                    if next_pos_vector.x < current_pos.x:
                        self.moving_right = False

            direction = (next_pos_vector - current_pos).normalize()  # get normalized vector from current to next pos
            current_pos += speed * direction  # increment current position along the diretion vector

            self.x, self.y = current_pos

            self.animation_step = (self.animation_step + 1) % (len(self.images))  # animation 000 to 009

    def hit(self, damage):
        self.current_health -= damage

        return self.current_health <= 0

    def get_value(self):
        '''
        Return value of enemy, to increase money
        :return: int
        '''
        return self.value

    def prepare_images(self):
        images = []
        for i in range(10):
            images.append(os.path.join("game_assets", "enemies", self.name, "1_enemies_1_WALK_{:03d}.png".format(i)))
        return images