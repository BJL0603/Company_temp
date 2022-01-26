# 敌方飞机模块
import pygame
import pygame.sprite   # 碰撞检测类
import pygame.image
import pygame.time
import pygame.mixer
import pygame.event
import pygame.display
import pygame.mask
import random

# 小型敌机的类
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        # 初始化碰撞检测类
        pygame.sprite.Sprite.__init__(self)

        # 加载地敌方小飞机图片
        self.image = pygame.image.load('images/enemy1.png').convert_alpha()
        # 添加摧毁时的图片
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy1_down1.png').convert_alpha(),
            pygame.image.load('images/enemy1_down2.png').convert_alpha(),
            pygame.image.load('images/enemy1_down3.png').convert_alpha(),
            pygame.image.load('images/enemy1_down4.png').convert_alpha()
        ])

        # 获取敌方小飞机的限定矩形
        self.rect = self.image.get_rect()
        # 将传进来的参数bg_size变量本地化
        self.width, self.height = bg_size[0], bg_size[1]
        # 敌机速度
        self.speed = 2
        # 存活状态
        self.active = True

        # 设置碰撞到飞机本体才爆炸，而不是碰到限制矩形就爆炸
        self.mask = pygame.mask.from_surface(self.image)

        # 使小飞机随机出现     self.rect.top = random.randint(-5 * self.height, 0) 防止敌机出现在一排  随机在一个区域出现
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(-5 * self.height, 0)
    # 小敌机移动规则
    def move(self):
        # 如果移动没超过画面下部，则正常一直向下移动
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            # 超出画面后重置位置
            self.reset()

    # reset()方法    超出画面后重置位置
    def reset(self):
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(-3 * self.height, 0)
        self.active = True

# 中型敌机的类
class MidEnemy(pygame.sprite.Sprite):
    # 为中型飞机加上血量，因为后面都要用到这个属性，所以定义在类里面
    energy = 8
    def __init__(self, bg_size):
        # 初始化碰撞检测类
        pygame.sprite.Sprite.__init__(self)

        # 加载地敌方中飞机图片
        self.image = pygame.image.load('images/enemy2.png').convert_alpha()
        # 加载被击中时的特效图片
        self.image_hit = pygame.image.load('images/enemy2_hit.png').convert_alpha()
        self.image_hit
        # 添加摧毁时的图片
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy2_down1.png').convert_alpha(),
            pygame.image.load('images/enemy2_down2.png').convert_alpha(),
            pygame.image.load('images/enemy2_down3.png').convert_alpha(),
            pygame.image.load('images/enemy2_down4.png').convert_alpha()
        ])
        # 获取敌方中飞机的限定矩形
        self.rect = self.image.get_rect()
        # 将传进来的参数bg_size变量本地化
        self.width, self.height = bg_size[0], bg_size[1]
        # 敌机速度
        self.speed = 1
        # 存活状态
        self.active = True
        # 设置碰撞到飞机本体才爆炸，而不是碰到限制矩形就爆炸
        self.mask = pygame.mask.from_surface(self.image)
        # 飞机血量  要用类的方法引用
        self.energy = MidEnemy.energy
        # 加入一个属性记录飞机是否被击中  用于绘制被击中的特效图片
        self.hit = False

        # 使中飞机随机出现     self.rect.top = random.randint(-10 * self.height, -self.height) 防止敌机出现在一排
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(-10 * self.height, -self.height)
    # 中敌机移动规则
    def move(self):
        # 如果移动没超过画面下部，则正常一直向下移动
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            # 超出画面后重置位置
            self.reset()

    # reset()方法    超出画面后重置位置
    def reset(self):
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(-10 * self.height, -self.height)
        self.active = True
        # 重置飞机时重置血量
        self.energy = MidEnemy.energy


# 大型飞机的类
class BigEnemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self, bg_size):
        # 初始化碰撞检测类
        pygame.sprite.Sprite.__init__(self)

        # 加载敌方大飞机图片
        self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
        self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
        self.image_hit = pygame.image.load('images/enemy3_hit.png').convert_alpha()
        # 添加摧毁时的图片
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load('images/enemy3_down1.png').convert_alpha(),
            pygame.image.load('images/enemy3_down2.png').convert_alpha(),
            pygame.image.load('images/enemy3_down3.png').convert_alpha(),
            pygame.image.load('images/enemy3_down4.png').convert_alpha(),
            pygame.image.load('images/enemy3_down5.png').convert_alpha(),
            pygame.image.load('images/enemy3_down6.png').convert_alpha()
        ])
        # 获取敌方大飞机的限定矩形
        self.rect = self.image1.get_rect()
        # 将传进来的参数bg_size变量本地化
        self.width, self.height = bg_size[0], bg_size[1]
        # 敌机速度
        self.speed = 1
        # 存活状态
        self.active = True
        # 设置碰撞到飞机本体才爆炸，而不是碰到限制矩形就爆炸
        self.mask = pygame.mask.from_surface(self.image1)
        # 飞机血量  用类的方法引用类的属性
        self.energy = BigEnemy.energy
        # 加入一个属性记录飞机是否被击中  用于绘制被击中的特效图片  默认没有被击中
        self.hit = False

        # 使大飞机随机出现     self.rect.top = random.randint(-15 * self.height, -5 * self.height) 防止敌机出现在一排
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(-15 * self.height, -5 * self.height)
    # 大敌机移动规则
    def move(self):
        # 如果移动没超过画面下部，则正常一直向下移动
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            # 超出画面后重置位置
            self.reset()

    # reset()方法    超出画面后重置位置
    def reset(self):
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(-15 * self.height, -5 * self.height)
        self.active = True
        self.energy = BigEnemy.energy


