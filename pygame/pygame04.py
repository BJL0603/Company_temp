'''
-------------------------------------------------
# -*- coding: utf-8 -*-
# @Author:Lijunbo
# @Time:2022/1/28 1:00
# @File:pygame04.py
# @Project:Company_temp
# @Software:PyCharm
-------------------------------------------------
'''
# 让鱼受控制

import pygame
import pygame.display
import pygame.time
import sys
import pygame.transform
# from pygame.locals import *   把所有的常量名都导入进来
class Fish_view:
    def Fish_move(self):

        size = width, height = 600, 400  # 先宽度再高度
        speed = [-2, 1]  # 每次移动的像素位置
        bg = (255, 255, 255)  # 游戏窗口的RGB

        # 设置游戏的窗口大小
        # display.set_mode()  会返回一个Surface 对象，这里可以当作一个背景画布，后面可以填充颜色
        # display.set_mode(尺寸元组，设置可拖拽放大缩小)
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        # 设置窗口标题
        pygame.display.set_caption('鱼儿')

        # 全屏参数
        # fullscreen = False  后面debug改了代码，不用它了
        # 用户显示屏可显示的尺寸列表，第0个就是最大的尺寸
        full = pygame.display.list_modes()[0]

        # 加载图片  也会返回一个Surface 对象
        # 要让图片运动就是修改图片的位置
        old_img = pygame.image.load('./test_Fish.png')
        img = old_img  # 备份一个，后面要对原图片进行放大缩小，用原图不会对像素产生影响
        # 图片加载出来是反的，先翻转一下
        # 导入时鱼头默认是向右
        # （因为程序一运行就碰撞了左边界，导致开始就执行了翻转，所以我们先翻转一次，程序再翻转一次方向就对了）
        img = pygame.transform.flip(img, True, False)
        # 每一个Surface都有一个矩形对象，他用来表示Surface的大小和位置信息
        old_img_position = old_img.get_rect()  # 对图片进行初始化定位
        img_position = old_img_position  # 备份一个，后面要对原图片进行获取rect()的 width  height，用原图位置不会对像素产生影响

        # 设值按键时改变对象(鱼头)的朝向  后面改了代码，用speed[0] 获取鱼头方向
        # L_head = img        # 导入时鱼头默认是向右（其实是向左，因为程序一开始就碰撞了左边界）
        # R_head = pygame.transform.flip(img, True, False)

        # img 的方向状态
        img_state = 1
        # 其实运行起来后向右运行表示-1，因为一开始就碰撞了屏幕边缘，190行改变了向右的初始值

        # 设置放大缩小的比率
        ratio = 1.0

        # 让图片一直移动 就是让它进入死循环
        while True:
            # 先写如何退出
            # 用户的所有操作都会放入事件队列，遍历事件队列，查看是否有退出类型事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # 检测按键
                if event.type == pygame.KEYDOWN:
                    # 出错时F10 重置
                    if event.key == pygame.K_F10:
                        img_position = img.get_rect()

                    if event.key == pygame.K_LEFT:
                        # 判断鱼头的状态是否朝右，朝右就翻转，然后赋值img_state为朝左的 1
                        if img_state == -1:
                            img = pygame.transform.flip(img, True, False)
                            img_state = 1  # 翻转鱼头后同步更改鱼头朝向的值
                        speed = [-2, 0]  # 移动前的值减移动后的值
                    if event.key == pygame.K_RIGHT:
                        if img_state == 1:
                            img = pygame.transform.flip(img, True, False)
                            img_state = -1
                        speed = [2, 0]
                    if event.key == pygame.K_UP:
                        speed = [0, -2]
                    if event.key == pygame.K_DOWN:
                        speed = [0, 2]

                    # img_position.right  图片右边至窗口左边的距离
                    # img_position.bottom 图片下边至窗口底部的距离
                    # img_position.left 图片左边至窗口左边的距离
                    # img_position.top  图片上边至窗口上边的距离
                    # img_position.width  图片矩形的宽
                    # img_position.height 图片矩形的高

                    # 全屏F11
                    if event.key == pygame.K_F11:
                        # fullscreen = not fullscreen
                        # 判断是否点了窗口右上角最大化按钮全屏，true就返回小屏
                        if width == full[0] and height + 53 == full[1]:
                            size = width, height = 600, 400
                            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                            # 还原为小屏时判断图片是否在小屏区域外
                            # 是就对图片重新定位，否就不用重来
                            if img_position.right > width or img_position.bottom > height:
                                img_position = img.get_rect()
                        # 判断是否处于全屏状态，true就返回小屏
                        elif width == full[0] and height == full[1]:
                            size = width, height = 600, 400
                            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                            # 还原为小屏时判断图片是否在小屏区域外
                            # 是就对图片重新定位，否就不用重来
                            if img_position.right > width or img_position.bottom > height:
                                img_position = old_img_position
                        # 处于小屏时按下F11 就全屏
                        else:
                            screen = pygame.display.set_mode((full), pygame.FULLSCREEN | pygame.HWSURFACE)
                            size = width, height = full[0], full[1]
                            '''
                            bug0.F11 切回小屏时窗口总是自动定位到左上角
                            bug1.存在一个BUG，就是先按下窗口最大化按钮，再按下F11退出全屏，窗口就无法拖动来调节大小
                            bug2.处于边缘时一直向边界按方向键，会卡死   已解决  181行
                            '''
                    # 放大缩小对象（-、=），空格恢复原始大小
                    # K_EQUALS  表示 = ，K_MINUS表示 -
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_MINUS or event.key == pygame.K_SPACE:
                        # 最大只能放大一倍,缩小只能0.5
                        if event.key == pygame.K_EQUALS and ratio < 2:
                            ratio += 0.1
                        if event.key == pygame.K_MINUS and ratio > 0.5:
                            ratio -= 0.1
                        if event.key == pygame.K_SPACE:
                            ratio = 1.0
                        # 使用较为精准的smoothscale(对象，(参数1，参数2)) 方法参数需要为int 类型
                        # transform.smoothscale()
                        '''
                        img = pygame.transform.smoothscale(old_img, 
                        (int(old_img_position.width * ratio), int(old_img_position.height * ratio)))
                        img_state = -1
                        '''
                        # 上下移动时判断鱼头的朝向，朝右就直接放大备份图片
                        if img_state == -1:
                            img = pygame.transform.smoothscale(old_img, (
                            int(old_img_position.width * ratio), int(old_img_position.height * ratio)))
                        # 朝左则先翻转备份图片再放大，再将备份图片翻转回初始方向
                        if img_state == 1:
                            old_img = pygame.transform.flip(old_img, True, False)
                            img = pygame.transform.smoothscale(old_img, (
                            int(old_img_position.width * ratio), int(old_img_position.height * ratio)))
                            old_img = pygame.transform.flip(old_img, True, False)  # 恢复为初始状态，用于下次判断

                        # 判断鱼是往右游还是左游
                        # 右游时鱼头为导入时默认不变
                        if speed[0] > 0:  # 判断X 的正负，正为右游，反之左游
                            img = img
                        # 左游时判断鱼头是否朝右，朝右就翻转，并改变状态值
                        if speed[0] < 0:
                            if img_state == -1:  # 朝右才翻转
                                img = pygame.transform.flip(img, True, False)
                                img_state = 1

                        # 放大或缩小后修改矩阵的宽和高
                        img_position.width = int(old_img_position.width * ratio)
                        img_position.height = int(old_img_position.height * ratio)

                        # 在接近边缘时放大图像会将图片卡在边上
                        # 所以判断放大后是否超过了窗口的高宽,是就将 图片右边至窗口左边的距离设为screen的宽，防止卡住
                        if img_position.right > width:
                            img_position.right = width
                        if img_position.bottom > height:
                            img_position.bottom = height

                # 用户拖拽调整窗口大小
                if event.type == pygame.VIDEORESIZE:
                    size = event.size
                    width, height = size

                    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                    # 写这个是为了防止鱼卡在屏幕边缘
                    if img_position.right > width:
                        # 如果拖拽时鱼的X 向被截断，就将鱼重新绘制
                        # 改变鱼右边位置为屏幕拖拽设置时的大小
                        img_position.right = width
                    if img_position.bottom > height:
                        # 拖拽时鱼的Y 向被截断，同上
                        img_position.bottom = height
                    # 右上角超出位置就初始化位置
                    if img_position.top < 0 or img_position.left < 0:
                        img_position = old_img_position

            # 让图片动起来
            img_position = img_position.move(speed)
            # 边界按方向键超出窗口卡死时重新将图片放到初始位置
            while img_position.right > width + 3 or img_position.bottom > height + 3 \
                    or img_position.left < -3 or img_position.top < -3:
                img_position = img.get_rect()
                break

            # 判断图片的位置是否左右碰撞，碰撞后翻转图片，并反方向移动
            if img_position.left < 0:
                # 如果碰撞边界就翻转图片
                # pygame.transform.flip(翻转(Surface对象)对象, True, False)，第二个是否水平翻转，第二个是否垂直翻转
                img = pygame.transform.flip(img, True, False)
                # 碰撞后反方向移动  就是将每次移动的左右像素值改为相反数
                speed[0] = -speed[0]
                img_state = -1
            if img_position.right > width:
                img = pygame.transform.flip(img, True, False)
                speed[0] = -speed[0]
                img_state = 1

            # 判断是否上下碰撞
            if img_position.top < 0 or img_position.bottom > height:
                # 上下达到界限时 将每次移动的上下像素值改为相反数
                speed[1] = -speed[1]

            # 填充游戏背景
            screen.fill(bg)
            # 每次移动后更新图像位置
            # 窗口名.blit()  就是把一个Surface 对象画到另一个Surface 上
            screen.blit(img, img_position)
            # 更新界面
            # 将上面两个放入内存中，然后调用 pygame.display.flip(),一次性输出在屏幕上，
            # 好处是加快绘图速度，避免闪烁现象（复杂图像时出现）
            pygame.display.flip()

            # 延迟刷新方法一
            # 每次循环休息15毫秒  delay()延迟方法
            # pygame.time.delay(15)

            # 延迟刷新方法二
            # 表示每分钟不高于100帧   一秒钟更新最多100帧
            pygame.time.Clock().tick(100)

if __name__ == '__main__':
    a = Fish_view()
    a.Fish_move()
    # 初始化pygame中的模块   随时待命工作
    pygame.init()
