import time
import pygetwindow as gw
import win32gui
import win32ui
import win32con  # 引入 win32con
from PIL import Image
import pytesseract
import numpy as np
import pyautogui
import os
import sys
import time
import shutil
import keyboard
ready_words=None
unready_words=None
langPack=None

import json

def init(json_file):
    global ready_words,unready_words,langPack
    with open(json_file, 'r') as file:
        data = json.load(file)
        ready_words = tuple(data["ready"])
        unready_words = tuple(data["unready"])
        langPack = data["lang"]


def capture_window(title):
    try:
        # 使用pygetwindow找到窗口
        window = gw.getWindowsWithTitle(title)[0]

        # 獲取窗口句柄
        hwnd = win32gui.FindWindow(None, window.title) 
    
        # 獲取窗口DC
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        # 創建位圖
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, window.width, window.height)
        cDC.SelectObject(dataBitMap)

        # 從窗口DC複製圖像
        cDC.BitBlt((0, 0), (window.width, window.height), dcObj, (0, 0), win32con.SRCCOPY)

        # 將位圖轉換為PIL圖像
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # 清理
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        im.save("full.png")
        # 保存圖像
        return im

    except Exception as e:
        print(f"Cropping {title} image error!!!: {e}")
        time.sleep(3)
        return None


def bring_to_foreground(window_title):
    # 定义一个回调函数，用于枚举窗口
    def enum_window_callback(hwnd, data):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_title:
            data.append(hwnd)

    # 枚举所有窗口，寻找匹配的窗口标题
    handles = []
    win32gui.EnumWindows(enum_window_callback, handles)

    # 如果找到了窗口，将其置于最前台
    if handles:
        win32gui.ShowWindow(handles[0], win32con.SW_RESTORE)  # 恢复窗口（如果最小化）
        win32gui.SetForegroundWindow(handles[0])
    else:
        print(f"No window with title '{window_title}' found.")


def get_window_position(window_title):
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        return win.left, win.top, win.width, win.height
    except IndexError:
        print(f"No window with title {window_title} found.")
        return None
    
def mark_click_position(x, y, duration=10):
    pyautogui.draw.circle(x, y, radius=10, color='red', duration=duration)

def click_relative(window_title, relative_rx, relative_ry):
    window_pos = get_window_position(window_title)
    if window_pos:
        x1, y1, w, h = window_pos
        pyautogui.click(x1+w*relative_rx, y1+h*relative_ry)

def touch(windows,rx,ry):
    bring_to_foreground(windows)
    click_relative(windows,rx, ry)


import Levenshtein

def levenshtein_similarity(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    max_len = max(len(str1), len(str2))
    if max_len == 0:  # 防止除以零
        return 1
    return 1 - distance / max_len

def find_similar_player(name, player_list, threshold=0.5):
    for player in player_list:
        if levenshtein_similarity(name, player['name']) >= threshold:
            return player
    return None

def update(player_list, data):
    for d in data:
        if(":" not in d):
            continue
        name, msg = d.split(':', 1)
        name=name.strip()
        if('#' not in name):
            continue
        similar_player = find_similar_player(name, player_list)

        if similar_player is not None:
            # 更新已有玩家的状态
            if any(substring.upper() in msg.upper() for substring in ready_words):
                similar_player['status'] = "ready"
            if any(substring.upper() in msg.upper() for substring in unready_words):
                similar_player['status'] = "unready"
        else:
            # 添加新玩家
            if any(substring.upper() in msg.upper() for substring in ready_words):
                new_status = "ready" 
            else:
                new_status="unready"
            new_player = {'name': name, 'status': new_status}
            player_list.append(new_player)


# 定義一個函數來清除終端屏幕
def clear_screen():
    # 對於Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # 對於mac和linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
import unicodedata
def visual_length(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)

def format_player_info(name, status, name_width, status_width):
    total_width = name_width + status_width + 4  # 包括 " -> " 和两边空格
    visual_len = visual_length(name) + visual_length(status)
    padding = total_width - visual_len
    return ' ' * (padding // 2) + f'{name} -> {status}' + ' ' * (padding - padding // 2)


def print_full_width(text, fill_char='_'):
    # 获取终端的宽度
    terminal_width, _ = shutil.get_terminal_size((80, 20))  # 默认值为80x20

    # 计算需要填充的字符数量
    text_length = len(text.encode('utf-8'))  # 为了正确处理中文字符
    padding_length = (terminal_width - text_length) // 2 - 1  # 减1是为了在另一边也有填充

    # 构造并打印填满整行的字符串
    full_width_str = fill_char * padding_length + text + fill_char * padding_length
    print(full_width_str)


def update_terminal(player_list):
    clear_screen()
    if not player_list:
        print_full_width(" [No Player @_@] ")
    else:
        
        name_width = 15
        status_width = 8
        print_full_width(f" Queue Waiting / number of player : {num_of_player}  ")
        print("")
        for i in range(0, len(player_list), 3):
            players_in_row = player_list[i:i + 3]

            row_parts = [format_player_info(player["name"], player["status"], name_width, status_width) for player in players_in_row]

            # while len(row_parts) < 3:
            #     row_parts.append(' ' * (name_width + status_width + 8))

            row_str = ' | '.join(row_parts)
            print(row_str)
    print("")
    print_full_width(f" [Press ESC to exit.] ")
    sys.stdout.flush()


def Check(player_List):
    if(len(player_List)!=num_of_player):
        return 0
    for player in player_List:
        if(player['status']=="unready"):
            return 0
    return 1

if(__name__=='__main__'):
    
    init("config.json")
    Status="Checking"
    while(1):
        if(Status=="Checking"):
            clear_screen()
            player_List=[]
            num_of_player=int(input("num of player:"))
            Status="waiting"
        screenshot=capture_window("League of Legends")
        if keyboard.is_pressed('esc'):
            Status = "Checking"
        if screenshot:
            #chat area
            left = 0
            top = screenshot.height - screenshot.height // 5.3
            right = int(screenshot.width / 4)
            bottom = screenshot.height*9.2//10
            cropped_image = screenshot.crop((left, top, right, bottom))

            cropped_image.save('crop.png')
            # pytesseract OCR
            text = pytesseract.image_to_string(cropped_image,lang=langPack)
            line=[txt for txt in text.split("\n") if len(txt)!=0]

            update(player_List,line)
            update_terminal(player_List)
            if(Check(player_List)):
                Status="Checking"
                touch("League of Legends",0.42,0.95)
                print_full_width("Game start!!!")
                time.sleep(2)
        else:
            Status="Checking"

