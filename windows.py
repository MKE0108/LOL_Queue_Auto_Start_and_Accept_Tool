import time
import pygetwindow as gw
import win32gui
import win32ui
import win32con  
from PIL import Image
import pyautogui
import time
import numpy as np


def capture_window(title):
    try:
        bring_to_foreground(title)
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
        #to cv2
        # 清理
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        return np.array(im)

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
        # win32gui.SetForegroundWindow(handles[0])
    else:
        print(f"No window with title '{window_title}' found.")


def get_window_position(window_title):
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        return win.left, win.top, win.width, win.height
    except IndexError:
        print(f"No window with title {window_title} found.")
        return None




def click_relative(window_title, relative_rx, relative_ry):
    window_pos = get_window_position(window_title)
    if window_pos:
        x1, y1, w, h = window_pos
        pyautogui.click(x1+w*relative_rx, y1+h*relative_ry)

def touch(windows,rx,ry):
    bring_to_foreground(windows)
    click_relative(windows,rx, ry)

