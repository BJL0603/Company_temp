import pygame
import pygame.image
import pygame.sprite
import random
import pygame.mask

class Bomb_Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bomb_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = random.randint(0, self.width - self.rect.width), -100

        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
        self.speed = 5

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.rect.left, self.rect.bottom = random.randint(0, self.width - self.rect.width), -100
        self.active = True
# 双枪补给类
class Bullet_Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = random.randint(0, self.width - self.rect.width), -100

        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
        self.speed = 5

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.rect.left, self.rect.bottom = random.randint(0, self.width - self.rect.width), -100
        self.active = True
