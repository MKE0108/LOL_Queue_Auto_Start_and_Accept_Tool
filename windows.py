import time
import pygetwindow as gw
import win32gui
import win32ui
import win32con  
from PIL import Image
import pyautogui
import time
import numpy as np
from cv2 import cvtColor, COLOR_RGB2BGR
def capture_window(title):
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
    
    return cvtColor(np.array(im), COLOR_RGB2BGR)




def bring_to_foreground_force(window_title):
    handle = win32gui.FindWindow(None, window_title)
    if handle == 0 :
        print(f"No window with title {window_title} found.")
        return
    win32gui.ShowWindow(handle, win32con.SW_NORMAL)
    win32gui.SetForegroundWindow(handle)


def bring_to_foreground(window_title):
    handle = win32gui.FindWindow(None, window_title)
    if handle == 0 :
        print(f"No window with title {window_title} found.")
        return
    win32gui.ShowWindow(handle, win32con.SW_NORMAL)

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
    for i in range(10):
        try:
            bring_to_foreground_force(windows)
            click_relative(windows,rx, ry)
            break
        except:
            print(f"No window with title {windows} found.")
            time.sleep(0.1)
    click_relative(windows,rx, ry)

