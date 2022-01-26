# 我方飞机模块
import pygame
import pygame.sprite   # 碰撞检测类
import pygame.image
import pygame.time
import pygame.mixer
import pygame.event
import pygame.display

# 定义一个类   继承pygame.sprite.Sprite   用于后面碰撞检测
class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        # 初始化碰撞检测类
        pygame.sprite.Sprite.__init__(self)

        # 加载我方飞机图片至画面中下位置  这儿右两张图片是因为向展现出尾气突突突  所以只是两张图片不停的切换
        self.image1 = pygame.image.load('images/me1.png').convert_alpha()
        self.image2 = pygame.image.load('images/me2.png').convert_alpha()
        # 添加摧毁图片
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy1_down1.png').convert_alpha(),
            pygame.image.load('images/enemy1_down2.png').convert_alpha(),
            pygame.image.load('images/enemy1_down3.png').convert_alpha(),
            pygame.image.load('images/enemy1_down4.png').convert_alpha(),
        ])
        # 获取我方飞机的限定矩形
        self.rect = self.image1.get_rect()

        # 将传进来的参数bg_size变量本地化
        self.width, self.height = bg_size[0], bg_size[1]
        # 定义我方飞机在中下位置， 画面下方有一个状态栏 预留60像素
        self.rect.left, self.rect.top = (bg_size[0] - self.rect.width) // 2, bg_size[1] - self.rect.height - 45

        # 设置我方飞机的移动速度
        self.speed = 10
        # 存活状态
        self.active = True
        # 设置碰撞到飞机本体才爆炸，而不是碰到限制矩形就爆炸
        self.mask = pygame.mask.from_surface(self.image1)

        # 记录我方飞机是否无敌
        self.invincible = False

    # 定义四个方法描述飞机的上下左右移动
    # 飞机上移时判断
    def moveUp(self):
        # 如果没有上移中没有超出画面
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0
    # 飞机下移时判断
    def moveDown(self):
        if self.rect.bottom < self.height - 45:
            self.rect.top += self.speed
        else:
            # 记得减去预留的状态栏
            self.rect.bottom = self.height - 45
    # 飞机左移时判断
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
    # 飞机右移时判断
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width
    # 飞机重生
    def reset(self):
        # 定义我方飞机在中下位置， 画面下方有一个状态栏 预留60像素
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 45
        self.active = True
        # 重生后无敌
        self.invincible = True
















