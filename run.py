import time
import pygetwindow as gw
import win32gui
import win32ui
import win32con  # 引入 win32con
from PIL import Image
import pytesseract
import numpy as np
import pyautogui


ready_words=None
unready_words=None


import json

def init(json_file):
    global ready_words,unready_words
    with open(json_file, 'r') as file:
        data = json.load(file)
        ready_words = tuple(data["ready"])
        unready_words = tuple(data["unready"])



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
        print(f"無法截取 {title}: {e}")
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
    print("Start!!!!")


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
                similar_player['status'] = 1 
            if any(substring.upper() in msg.upper() for substring in unready_words):
                similar_player['status'] = 0
        else:
            # 添加新玩家
            if any(substring.upper() in msg.upper() for substring in ready_words):
                new_status = 1 
            else:
                new_status=0
            new_player = {'name': name, 'status': new_status}
            player_list.append(new_player)



def Check(player_List):
    if(len(player_List)!=num_of_player):
        return 0
    for player in player_List:
        if(not player['status']):
            return 0
    return 1

if(__name__=='__main__'):
    lastMsg=""
    init("config.json")
    Status="Checking"
    while(1):
        if(Status=="Checking"):
            player_List=[]
            num_of_player=int(input("num of player?"))
            Status="waiting"
        screenshot=capture_window("League of Legends")
        if screenshot:
            #chat area
            left = 0
            top = screenshot.height - screenshot.height // 5.3
            right = int(screenshot.width / 4)
            bottom = screenshot.height*9.2//10
            cropped_image = screenshot.crop((left, top, right, bottom))

            cropped_image.save('crop.png')
            # pytesseract OCR
            text = pytesseract.image_to_string(cropped_image,lang='chi_tra')
            line=[txt for txt in text.split("\n") if len(txt)!=0]
            # print("text:")
            # print(line)
            update(player_List,line)
            tmpMsg=""
            for player in player_List:
                tmpMsg+=f'{player["name"]}->{player["status"  ]}\n'
            if(tmpMsg!=lastMsg):
                print("!!!update!!!")
                print(tmpMsg)
                lastMsg=tmpMsg
            if(Check(player_List)):
                Status="Checking"
                touch("League of Legends",0.42,0.95)
        else:
            Status="Checking"

