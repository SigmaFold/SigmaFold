from pyautogui import * 
import pyautogui as pg
#include functions.py
import time 
import random
import win32api, win32con
import keyboard
from pynput.keyboard import Listener
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from pyclick import HumanClicker
import numpy as np
hc = HumanClicker()
sleep(1)



while keyboard.is_pressed('q')!= True: #if q button is pressed, it stops
    pic = pg.screenshot(region=(450,350,1300,700)) #takes screenshot in a region x=450 y=350 coords and 450+1300, 350+700 rectangle

    for x in range(0,1300,60): #loop to search for all pixels in the variable pic
        for y in range(0,700,50): 
            
            r,g,b= pic.getpixel((x,y)) #collect r g b values of 1 pixel

            if b==232:  #if blue value is 232 color of the target
                win32api.SetCursorPos((x+450,y+350)) #cursor mouves to cords of the pixel
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) #left click
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0) #left click up
                break #and gets back to while loop


# pic_prev = pg.screenshot(region=(...))

# while True:
#     temp_pic = pg.screenshot(region=(450,350,1300,700))
#     diff = pic_prev - temp_pic
#     if np.sum(diff) == 0:
#         pass
#     else:
#         m, n = np.nonzero(diff)


