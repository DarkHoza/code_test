import pyautogui
import time
import random

while True:
    pyautogui.FAILSAFE = True
    screenW, screenH = pyautogui.size()
    temp_x, temp_y = pyautogui.position()
    time.sleep(145)
    current_x, current_y = pyautogui.position()
    if temp_x == current_x and temp_y == current_y:
        ran_w = random.randint(1, screenW)
        ran_h = random.randint(1, screenH)

        pyautogui.moveTo(ran_w, ran_h, 0.3)
        pyautogui.typewrite(" ", 1)
        # print(temp_x, temp_y)
        # print(current_x, current_y)     