import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import cv2
from windows import get_window_position,bring_to_foreground,touch,capture_window
import keyboard
from termUI import clear_screen,visual_length,format_player_info,print_full_width,update_terminal
from textCmp import levenshtein_similarity,find_similar_name_from_list
from paddleocr import PaddleOCR, draw_ocr
import cv2
import time
ocr = None
ready_words=None
unready_words=None
langPack=None
running = False
import json
def init(json_file):
    global ready_words,unready_words,langPack,ocr
    with open(json_file, 'r') as file:
        data = json.load(file)
        ready_words = tuple(data["ready"])
        unready_words = tuple(data["unready"])
        langPack = data["lang"]
    


#get current player
def get_current_player(img:np.array):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _,img = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)
    #find current player
    players = []
    positions = [[655/1920,550/1080,275/1920,45/1080],
                 [370/1920,525/1080,275/1920,45/1080],
                 [(370+(370-675))/1920,525/1080,275/1920,45/1080],
                 [962/1920,525/1080,275/1920,45/1080],
                 [(962+(962-665))/1920,525/1080,275/1920,45/1080],
                 ]
    for p in positions:
        x,y,w,h = p
        text = pytesseract.image_to_string(img[int(y*img.shape[0]):int((y+h)*img.shape[0]),int(x*img.shape[1]):int((x+w)*img.shape[1])],lang=langPack)
        player=[txt.strip() for txt in text.split("\n") if len(txt.strip())!=0]
        if(len(player)!=0):
            players.append(player[0])
    return players

def get_chat_message(screenshot:np.array):
    #chat area
    left = 0
    top = screenshot.shape[0] - screenshot.shape[0] // 5.3
    right = int(screenshot.shape[1] / 4)
    bottom = screenshot.shape[0]*9.2//10

    cropped_image = screenshot[int(top):int(bottom),int(left):int(right)]
    cropped_image=cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    # pytesseract OCR
    text = pytesseract.image_to_string(cropped_image,lang=langPack,config='--psm 6')
    line=[txt.strip() for txt in text.split("\n") if len(txt.strip())!=0]
    return line

def update(player_list, data):
    for d in data:
        if(":" not in d):
            continue
        name, msg = d.split(':', 1)
        name=name.strip()
        if('#' not in name):
            continue
        name="#".join(name.split('#')[:-1])
        similar_player = find_similar_name_from_list(name, [p['name'] for p in  player_list])
        player = next((player for player in player_list if player['name'] == similar_player), None)
        if player:
            if any(word in msg for word in ready_words):
                player['status'] = 'ready'
            elif any(word in msg for word in unready_words):
                player['status'] = 'unready'

def on_press(e):
    global running
    if e.name == 's':
        running = True
    elif e.name == 'esc':
        running = False

keyboard.on_press(on_press)

if(__name__=='__main__'):
    running = False
    try:
        init("config.json")
        player_list=[]
        while(1):
            if running:
                players=get_current_player(capture_window("League of Legends"))
                for player in players:
                    if player not in [p['name'] for p in player_list]:
                        player_list.append({"name":player,"status":"unready"})
                for player in player_list:
                    if player['name'] not in players:
                        player_list.remove(player)
                msg=get_chat_message(capture_window("League of Legends"))
                time.sleep(0.5)
                update(player_list,msg)
                update_terminal(player_list)
                if(all(player['status'] == "ready" for player in player_list)):
                    touch("League of Legends",0.42,0.95)
                    running = False
            else:
                clear_screen()
                player_list=[]
                print_full_width("Press 's' to start")
                continue

    except Exception as e:
        print(f"Error info->{e}")

