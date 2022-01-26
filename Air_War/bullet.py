# 子弹模块
import pygame
import pygame.sprite   # 碰撞检测类
import pygame.image
import pygame.time
import pygame.mixer
import pygame.event
import pygame.display
import pygame.mask

#
# 生成单枪子弹的类
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        # 记录子弹的存活状态
        self.active = False
        # 撞击到子弹本体才摧毁
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        # 当子弹底部坐标为0时，设置为子弹摧毁
        if self.rect.top < 0:
            self.active = False

    # 重置子弹位置时传入飞机位置参数
    def reset(self, position):
        self.active = True
        self.rect.left, self.rect.top = position

# 生成双枪子弹的类
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 14

        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True







