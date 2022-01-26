import pygame
import pygame.image
import pygame.time
import pygame.mixer
import pygame.event
import pygame.display
import pygame.key
# 导入pygame的全部常量模块
from pygame.locals import *
import pygame.sprite
import pygame.mask
import pygame.draw
import pygame.font

import sys
import traceback   # 异常捕捉模块
import myplane
import enemy
import bullet
import supply
import random

# 游戏模块初始化
pygame.init()
# 混音器初始化
pygame.mixer.init()

# 定义游戏画面大小
bg_size = width, height = 480, 700
# 设置游戏屏幕大小
screen =  pygame.display.set_mode(bg_size)
# 设置游戏标题
pygame.display.set_caption('飞机大战 -- Demo')

background = pygame.image.load('images/background.png').convert_alpha()

# 音乐和音效
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.3)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

# 用于下面增加游戏难度的方法  和实例化飞机
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        # group() 用add   列表用append
        group1.add(e1)
        group2.add(e1)

# 用于下面增加游戏难度的方法  和实例化飞机
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

# 用于下面增加游戏难度的方法   和实例化飞机
def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)
# 增加目标机型的速度
def inc_speed(target, inc):
    for i in target:
        i.speed += inc

# 主函数
def main():
    # 无限循环播放音乐
    pygame.mixer.music.play(-1)
    # 设置游戏帧率参数
    clock = pygame.time.Clock()
    # 用于切换飞机图片  达到动态在突突突的飞行效果
    switch_image = True
    # 因为图片切换看不出效果  所以加一个延迟  毫秒
    delay = 100

    # 生成我方飞机对象
    me = myplane.MyPlane(bg_size)
    # 生成一个敌方飞机的Group，用于之后的碰撞检测
    enemies = pygame.sprite.Group()

    # 生成小飞机对象   一枪一个
    small_enemies = pygame.sprite.Group()
    # 用于后面增加游戏难度和初始化飞机个数
    add_small_enemies(small_enemies, enemies, 15)

    # 生成中飞机对象  多枪一个
    mid_enemies = pygame.sprite.Group()
    # 用于后面增加游戏难度和初始化飞机个数
    add_mid_enemies(mid_enemies, enemies, 20)

    # 生成大飞机对象   超多枪一个
    big_enemies = pygame.sprite.Group()
    # 用于后面增加游戏难度和初始化飞机个数
    add_big_enemies(big_enemies, enemies, 10)

    # 敌机中弹/摧毁 时图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 实例化子弹
    # 子弹数
    bullet1 = []
    BULLET1_NUM = 4
    bullet1_index = 0
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 定义几个颜色，用于后面绘制飞机血量
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)     # 分数的颜色(score)

    # 统计得分
    score = 0
    # 分数用的字体样式 和 字体大小
    score_font = pygame.font.Font('font/font.ttf', 36)

    # 实现一个暂停和继续游戏的功能
    # 设置一个参数用来标志是否暂停游戏
    paused = False

    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()   # 图一
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()# 鼠标放置在图一上时，显示这个动效图片，增加互动性
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()  # 图二
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()# 鼠标放置在图二上时，显示这个动效图片，增加互动性
    # 获取一个图片的限定矩形（四个大小都一样）
    paused_rect = pause_nor_image.get_rect()
    # 暂停继续放在右上角( 减10 是为了美观)
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    # 设置默认显示  (默认右上角显示没有把鼠标放在暂停图片上的图片)
    paused_image = pause_nor_image

    # 增加调整游戏难度的参数
    level = 1
    # 增加全屏炸弹左下角字样
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left, bomb_rect.top = 10, height - 10 - bomb_rect.height
    bomd_font = pygame.font.Font('font/font.ttf', 36)
    bomb_num = 3

    # 增加炸弹和双枪支援
    # 实例化双枪补给
    double_supply = supply.Bullet_Supply(bg_size)
    # 实例化炸弹补给
    bomb_supply = supply.Bomb_Supply(bg_size)
    # 添加自定义事件 用来控制每30 秒提供一次支援
    Supply_EVENT = pygame.USEREVENT
    pygame.time.set_timer(Supply_EVENT, 10 * 1000)

    # 增加一个自定义时间事件用来记录双枪的持续时间
    Double_Bullet_Event = pygame.USEREVENT + 1
    # 增加一个变量用来记录是否使用超级子弹 默认为没有使用
    is_double_bullet = False
    # 实例化双枪子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    # 因为我们遍历一次添加两个子弹对象   所以BULLET2_NUM // 2
    for each in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery - 50)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery - 50)))

    # 设置一个参数，记录是否暂停过游戏
    # 用于后面支援事件继续从上次暂停的事件继续，而不是从头再计时
    # 没有实现，遗留BUG

    # 我方飞机生命的小图片
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_image_rect = life_image.get_rect()

    # 我方飞机生命数
    life_num = 3

    # 定义一个自定义事件，用于我方飞机重生后无敌三秒
    Invincible_Event = pygame.USEREVENT + 2

    # 定义一个参数，用来阻止结束时重复打开和关闭文件
    recorded = False

    # 游戏结束时的按钮图片
    gameover_font = pygame.font.Font('font/font.ttf', 48)       # 重写一次是因为与上次的大小不一样
    again_image = pygame.image.load('images/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 用更好的退出方式
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检测鼠标 当前的点是否放置在图片限定矩形上 并且是否按下了左键
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    # 这儿添加的代码用来暂停游戏时停止背景音乐和音效
                    if paused:
                        # 停背景音乐
                        pygame.mixer.music.pause()
                        # 停音效（大飞机出生音效）
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()


            if event.type == pygame.MOUSEMOTION:
                # 检测鼠标当前的点是否放置在图片限定矩形上
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        pygame.mixer.music.unpause()
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            if event.type == pygame.KEYDOWN:
                # 检测是否是激活状态 且 是否按下了空格键
                if event.key == pygame.K_SPACE and not paused:
                    # 有炸弹才能执行
                    if bomb_num:
                        bomb_num -= 1
                        # 按下暂停键时遍历飞机 设置为摧毁状态
                        for i in enemies:
                            if i.rect.bottom > 0:
                                i.active = False
            # 检测到补给时间到时，随机投放
            if event.type == Supply_EVENT and not paused:
                supply_sound.play()
                # 随机选一个
                if random.choice([False, True]):
                    # True时，投放全屏炸弹
                    bomb_supply.reset()
                else:
                    # False 是，投放双枪子弹
                    double_supply.reset()
            # 检测是否产生了双枪事件
            if event.type == Double_Bullet_Event:
                # 拾取到双枪之后，计时器开始工作，工作五秒后再产生一个Double_Bullet_Event自定义事件，标志着持续时间结束
                is_double_bullet = False
                # 取消关注定时器
                pygame.time.set_timer(Double_Bullet_Event, 0)
            # 检测到我方飞机无敌时间结束  解除无敌
            if event.type == Invincible_Event:
                # 检测到结束时停止该事件  并解除无敌
                pygame.time.set_timer(Invincible_Event, 0)
                me.invincible = False

        # 绘制背景图至窗口 (0,0) 相对窗口的位置
        # 绘制在  if not paused: 前是因为在点击暂停之后需要将战局用background覆盖，防止用户通过频繁的暂停和开始来躲避敌机
        screen.blit(background, (0, 0))

        # 根据分数调整当前游戏难度
        if level == 1 and score > 50000:
            level = 2
            # 难度增加的提示音效
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 增加小型机速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 增加小、中型机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 增加小、中型机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        # 只有为True 才能运行
        if not paused and life_num:
            # 检测用户的键盘操作 (序列)    # 获取到的是键盘所有键的状态序列，存储每个键是否按下（True，False）
            # 频繁键盘事件用此方法
            key_pressed = pygame.key.get_pressed()

            # W 按键和上方向键都可以控制
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 如果随机到炸弹补给
            # 用一个对象前，先检测是否是我们想要的状态，是才执行
            if bomb_supply.active:
                screen.blit(bomb_supply.image, bomb_supply.rect)
                bomb_supply.move()
                # 检测两个精灵是否碰撞  pygame.sprite.collide_mask(精灵1， 精灵2)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    bomb_supply.active = False
                    # 拾取到全屏炸弹
                    get_bomb_sound.play()
                    # 检测炸弹数是否小于3，小于3个才增加
                    if bomb_num < 3:
                        bomb_num += 1
            # 如果随加到双枪补给
            if double_supply.active:
                screen.blit(double_supply.image, double_supply.rect)
                double_supply.move()
                if pygame.sprite.collide_mask(double_supply, me):
                    get_bullet_sound.play()
                    # 检测到拾取到补给后，设置记录双枪的变量为True，用来后面发射双枪
                    is_double_bullet = True
                    # 检测到拾取到双枪补给后，开始产生一个双枪自定义事件,五秒后再次产生一个此事件
                    pygame.time.set_timer(Double_Bullet_Event, 5 * 1000)
                    # 拾取到之后应设置属性为False
                    double_supply.active = False

            # 检测到双枪变量为True后
            if is_double_bullet:
                if not(delay % 10):
                    # 与单枪统一成一个列表，这样就能重复使用代码
                    bullets = bullet2
                    bullet_sound.play()
                    # 检测到双枪变量为True后，调用reset方法使子弹的active为True
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery - 50))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery - 50))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
            else:
                # 60帧里生成4子弹
                if not(delay % 10):
                    # 与双枪统一成一个列表，这样就能重复使用代码
                    bullets = bullet1
                    bullet_sound.play()
                    # 每过10帧重置一次子弹的位置，这样的话60帧里就能够画四个子弹了
                    bullets[bullet1_index].reset(me.rect.midtop)        # 传入自己飞机的中间位置，子弹就会随飞机移动
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 绘制敌机前检查是否被子弹击中
            for b in bullets:
                if b.active:
                    b.move()
                    if is_double_bullet:
                        screen.blit(b.image, b.rect)
                    else:
                        screen.blit(b.image, b.rect)
                    # 子弹存活时检测是否与敌机碰撞   放入列表中
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    # 遍历这儿列表  如果有碰撞的对象，则将其active设置为False
                    # 先判断一下是否有数据  有的话才遍历，这样节省资源
                    if enemy_hit:
                        # 子弹毁灭
                        b.active = False
                        # 敌机毁灭
                        for e in enemy_hit:
                            # 因为加入了中飞机大飞机的血量  所以这儿判断遍历出来的对象是否时大飞机  或  中飞机  是就在击中时减少一滴血
                            if (e in mid_enemies) or (e in big_enemies):
                                e.hit = True
                                e.energy -= 1
                                # 血量打为零后  设置飞机被击毁
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False


            # 首先绘制大飞机再绘制中 最后绘制小飞机，因为先绘制小，大会将其覆盖
            for each in big_enemies:
                # 检查是否时存活状态
                if each.active:
                    # 遍历出每一个调用移动方法
                    each.move()
                    # 飞机被击中时的那会儿绘制特效图片   正常时绘制正常图片
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    # 绘制完飞机之后绘制血量
                    # 先绘制一个黑色的血槽底槽   绘制在飞机限定矩形的上方5个像素处
                    pygame.draw.line(screen,(0,0,0),(each.rect.left,each.rect.top - 5),(each.rect.right, each.rect.top - 5),2)
                    # 计算飞机剩余血量
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    # 剩余血量小于20% 时绘制红色的血量
                    if energy_remain > 0.2:
                        energy_color = green
                    else:
                        energy_color = red
                    # 将剩余血量绘制在黑色底槽上方
                    # 剩余血量绘制开始的位置  (each.rect.left, each.rect.top - 5)
                    # 剩余血量绘制结束的位置  (each.rect.left + each.rect.width * enemgy_remain)
                    # 结束位置：将限定矩形的width分为20份(大飞机血量)
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),(each.rect.left + each.rect.width * energy_remain, each.rect.top - 5))

                    # 大飞机即将出现时播放音效  当下部等于50时播放，不能写为大于或者小于，因为写成这样的话会每一帧都播放一次，当毁灭后音效停止
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                    if each.rect.top == height:
                        enemy3_fly_sound.stop()
                else:
                    # 毁灭    被摧毁时或相撞时
                    # 每隔三帧  播放一帧毁灭的画面，播放完毕之后reset()
                    if not(delay % 3):
                        # 这儿加e3_destroy_index == 0 是因为主程序每循环一次，不加判断的话，就会再次播放音效详见下面的else
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        # 下面e3_destroy_index产生的有1，2，3，4，5，0，1，2.....
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            for each in mid_enemies:
                if each.active:
                    # 遍历出每一个调用移动方法
                    each.move()
                    # 子弹击中飞机时的那会儿绘制特效图片  正常时绘制正常图片
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制完飞机之后绘制血量
                    # 先绘制一个黑色的血槽底槽
                    pygame.draw.line(screen, (0,0,0),(each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)

                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = green
                    else:
                        energy_color = red
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5))

                else:
                    # 毁灭    被摧毁时或相撞时
                    # 每隔三帧  播放一帧毁灭的画面，播放完毕之后reset()
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        # 下面e2_destroy_index产生的有1，2，3，4，5，0，1，2.....
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 5000
                            each.reset()
            for each in small_enemies:
                if each.active:
                    # 遍历出每一个调用移动方法
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭    被摧毁时或相撞时
                    # 每隔三帧  播放一帧毁灭的画面，播放完毕之后reset()  99 96 93 90  86
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        # 下面e1_destroy_index产生的有1，2，3，4，5，0，1，2.....
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 在绘制我方飞机前检测是否被撞击
            # me与enemies列表中的精灵发生碰撞则返回enemies 中碰撞的精灵，我们用一个列表来接收
            # False 表示碰撞后删除对象，第四个参数表示指定检测碰撞的函数
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            # 如果存在相撞的对象
            if enemies_down and not me.invincible:
                # 则自方遇难
                me.active = False
                # 则将所有的敌机状态改为遇难状态
                for e in enemies_down:
                    e.active = False


            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭    被摧毁时或相撞时
                # 每隔三帧  播放一帧毁灭的画面，播放完毕之后reset()
                if not(delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(each.destroy_images[me_destroy_index], each.rect)
                    # 下面e3_destroy_index产生的有1，2，3，4，5，0，1，2.....
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        me.reset()
                        life_num -= 1
                        pygame.time.set_timer(Invincible_Event, 3 * 1000)
                        print('凉了一次！')

            # 绘制炸弹在里面，这样暂停的时候我们就看不到全屏炸弹的数量
            screen.blit(bomb_image, bomb_rect)
            # 绘制炸弹个数
            bomb_text = bomd_font.render('X %s' % str(bomb_num), True, white)
            screen.blit(bomb_text, (bomb_rect.width + 20, height - bomb_rect.height))

            # 绘制我方飞机后绘制分数至窗口
            # pygame中操做的都是surface对象，string文本.render(字符串对象，是否开启抗锯齿，字体颜色，字体背景色)   能将字符串转化为surface对象
            score_text = score_font.render('Score: %s' % str(score), True, white)
            # 绘制分数至窗口
            screen.blit(score_text, (10, 5))
            # 将暂停继续的图片绘制出来
            screen.blit(paused_image, paused_rect)


            # 检测到我方飞机生命为0时
            if life_num:
                # 绘制我方飞机的生命数量
                for m in range(life_num):
                    screen.blit(life_image, (width - life_image_rect.width * (m + 1) - 10, height - life_image_rect.height))
        # 绘制游戏结束画面   我放飞机生命用尽
        elif life_num == 0:
            # 停止音乐
            pygame.mixer.music.stop()
            # 停止音效
            pygame.mixer.stop()
            # 停止补给
            pygame.time.set_timer(Supply_EVENT, 0)
            # 读取历史最高得分   recorded是为了阻止重复打开和关闭文件
            if not recorded:
                recorded = True
                try:
                    with open('record.txt', 'r') as f:
                        pass
                        #record_score = f.read()

                # 如果记录的文件被用户删除时触发这儿
                except FileNotFoundError:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))
                finally:
                    with open('record.txt', 'r') as f:
                        record_score = f.read()
                    # 如果这次得分高于历史得分
                    if int(score) > int(record_score):
                        with open('record.txt', 'w') as f:
                            f.write(str(score))
                    # 最后读取一次存在文件里的分数
                    with open('record.txt', 'r') as f:
                        best_score = f.read()
                '''
                with open('record.txt', 'r') as f:
                    record_score = f.read()
                    #如果这次得分高于历史得分
                    if score > record_score:
                        with open('record.txt', 'wr') as f:
                            f.write(str(score))'''
            # 绘制结束画面
            record_score_text = score_font.render("Best: %d" % int(best_score), True, white)
            screen.blit(record_score_text, (50, 50))

            # 本局游戏结束时的分数  上面显示文字 下面分数
            gameover_text1 = gameover_font.render("Your score", True, white)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            # 本局游戏结束时的分数  下面显示分数   分数转化为str 类型
            gameover_text2 = gameover_font.render(str(score), True, white)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2,\
                                                                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            # 绘制结束时的两个按钮 第一个
            again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50      # 相对定位(相对本局结束分数的位置)
            screen.blit(again_image, again_rect)
            # 第二个
            gameover_rect.left, gameover_rect.top = (width - gameover_rect.width) // 2, again_rect.bottom + 10      # 相对上一个按钮的定位
            screen.blit(gameover_image, gameover_rect)

            # 游戏结束时检测用户鼠标是否点击了上面的按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and again_rect.collidepoint(event.pos):
                    main()
                if event.button == 1 and gameover_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()



        # 减帧方法
        # 能被5整除时才切换变量的值，从而达到限制帧率  延迟切换飞机突突突图片的效果
        if not(delay % 5):
            switch_image = not switch_image
        # 每一帧减一，因为我们这儿是一秒六十帧，所以一秒减少60，
        # 那么一秒钟就有12 个数字能被5 整除，所以就达到了限制帧率的目的（12帧）
        delay -= 1
        if not delay:
            delay = 100


        # screen只是绘制至了内存中，需要pygame.display.flip() 到显示器
        pygame.display.flip()
        # 定义游戏帧率
        clock.tick(60)
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # 点击×退出的异常不用关心
        pass
    except:
        # 其它异常时打印出错误之处后退出pygame模块， 打印出来后停留: input()
        traceback.print_exc()
        pygame.quit()
        input()
