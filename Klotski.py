# _*_ coding: utf-8 _*_
import pygame
from sys import exit
from os import environ as Environ
from pygame.locals import *
from sys import exit
from win32api import GetSystemMetrics as _getSystemMetrics
from random import randint as Randint
from time import sleep as Wait


# grid (57,170)
# 每一个小方块大小 92 * 92 px
# 总共原图大小 368 *368 px
# 缩略图大小： 95 * 95 px

def switchpos(origin_list, index_x, index_y): #交换图片位置
    if(index_x-1 >= 0):
        if(origin_list[index_x-1][index_y] == 0):
            origin_list[index_x-1][index_y] = origin_list[index_x][index_y]
            origin_list[index_x][index_y] = 0
    if(index_x+1 <= 3):
        if(origin_list[index_x+1][index_y] == 0):
            origin_list[index_x+1][index_y] = origin_list[index_x][index_y]
            origin_list[index_x][index_y] = 0   
    if(index_y-1 >= 0):
        if(origin_list[index_x][index_y-1] == 0):
            origin_list[index_x][index_y-1] = origin_list[index_x][index_y]
            origin_list[index_x][index_y] = 0
    if(index_y+1 <= 3):
        if(origin_list[index_x][index_y+1] == 0):
            origin_list[index_x][index_y+1] = origin_list[index_x][index_y]
            origin_list[index_x][index_y] = 0
    return origin_list 

def puzzleinit(): # 返回一个打乱的二维数组
    origin_list = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
    for i in range(150):
        index_x = Randint(0,3)
        index_y = Randint(0,3)
        switchpos(origin_list, index_x, index_y)
    return origin_list

def ifsuccess(list_now): #判断是否结束
    flag = 1
    for i in range(0,4):
        for j in range(0,4):
            if(list_now[i][j] != (i*4+j+1)%16):
                flag = 0
                break
    return flag  

def maingame(screen): # 游戏主循环
    alist = puzzleinit()
    picindex = Randint(1,4)
    # 游戏主循环
    while True:
        endcircle = 0
        cursor_x = 0
        cursor_y = 0
        flag = 0 #没有鼠标点击事件
        for event in pygame.event.get():
            if event.type == QUIT:
                # 接收到退出时间后退出程序
                exit(0)
            if event.type == MOUSEBUTTONDOWN:
                flag = 1 # 有鼠标点击事件
                cursor_x, cursor_y = pygame.mouse.get_pos()      # 获得鼠标位置

        if flag == 1:
            if(cursor_x>=149 and cursor_x < 149+92*2 and cursor_y>=564 and cursor_y<=564+45):
                endcircle = 1
                break
            elif( (cursor_x-57)//92 in range(0,4) and (cursor_y-170)//92 in range(0,4)):
                a = (cursor_x-57)//92
                b = (cursor_y-170)//92
                switchpos(alist, b, a)

        # 将背景图画上去
        screen.blit(background, (0, 0))

        # 画小方块
        for i in range(0,4):
            for j in range(0,4):
                image_name = './klotski_image/pics/pic_0'+ str(picindex) + '/' + str(alist[i][j]) + '.png'
                im = pygame.image.load(image_name)
                screen.blit(im, (58+j*92, 170+i*92))

        # 画格子        
        imgrid_name = './klotski_image/grid.png'
        imgrid = pygame.image.load(imgrid_name)
        screen.blit(imgrid, (57,170))

        # 画缩略图
        image_name = './klotski_image/pics/pic_0'+ str(picindex) + '/' + 'small.jpg'
        im = pygame.image.load(image_name)
        screen.blit(im, (320, 43))
        image_name = './klotski_image/Rect_origin.png'
        im = pygame.image.load(image_name)
        screen.blit(im, (320, 43))

        # 画重新开始按钮
        x, y = pygame.mouse.get_pos()
        if(x>=149 and x < 149+92*2 and y>=564 and y<=564+45):
            screen.blit(buttondown, (149, 564))
        else:
            screen.blit(buttonup, (149, 564))


        # cursor_x, cursor_y = pygame.mouse.get_pos()      # 获得鼠标位置
        # if(cursor_x>=149 and cursor_x < 58+92*2 and cursor_y):
            

        # 刷新画面
        flag = 0
        
        pygame.display.update()

        if ifsuccess(alist) == 1:
            endcircle = 1
            screen.blit(success, (0, 0))
            pygame.display.update()
            Wait(1)

        if endcircle == 1:
            break

if __name__ == '__main__':


    # 载入图片
    background_image_filename = './klotski_image/background.png' #背景
    mouse_image_filename = './klotski_image/cursor.png' #鼠标
    buttondown_image_filename = './klotski_image/buttondown.png'
    buttonup_image_filename = './klotski_image/buttonup.png'
    success_image_filename = './klotski_image/success.png'
    # 初始化pygame，为使用硬件做准备
    pygame.init()

    # 创建一个窗口
    current_w = _getSystemMetrics(0) #获得屏幕分辨率X轴  # win32con.SM_CXSCREEN
    current_h = _getSystemMetrics(1) #获得屏幕分辨率Y轴  # win32con.SM_CYSCREEN
    pos_x, pos_y = int((current_w-480)/2), int((current_h-640)/2)
    Environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (pos_x, pos_y)
    screen = pygame.display.set_mode((480, 640), 0, 32)

    # 设置窗口标题
    pygame.display.set_caption("Klotski_0707  by OS")

    # 加载图片并转换
    background = pygame.image.load(background_image_filename)
    mouse_cursor = pygame.image.load(mouse_image_filename)
    buttondown = pygame.image.load(buttondown_image_filename)
    buttonup = pygame.image.load(buttonup_image_filename)
    success = pygame.image.load(success_image_filename)

    while True:
        maingame(screen)
