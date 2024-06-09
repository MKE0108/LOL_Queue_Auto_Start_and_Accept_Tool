
from windows import get_window_position,bring_to_foreground,touch,capture_window
import keyboard
from termUI import clear_screen,print_full_width,update_auto_start_terminal,waiting_for_accept
from textCmp import levenshtein_similarity,find_similar_name_from_list
from imageProcess import get_ac_crop,get_current_player,get_chat_message,compare_image
import time
from enum import Enum
from cv2 import imread

class MODE(Enum):
    CHOSING=0
    AUTO_START=1
    AUTO_ACCEPT=2
    WAITING_ENTER_GAME=3
    QUIT=4
ac_image=None
current_mode = MODE.CHOSING
ready_words=None
unready_words=None
langPack=None
running = False
import json
def init(json_file):
    global ready_words,unready_words,langPack,ac_image
    with open(json_file, 'r') as file:
        ac_image=imread("ac_crop_1.png")
        data = json.load(file)
        ready_words = tuple(data["ready"])
        unready_words = tuple(data["unready"])
        langPack = data["lang"]

    
def update_plyer_list(player_list, data):
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
def maintain_player_list(player_list,players):
    for player in players:
        if player not in [p['name'] for p in player_list]:
            player_list.append({"name":player,"status":"unready"})
    for player in player_list:
        if player['name'] not in players:
                player_list.remove(player)
def on_press(e):
    global current_mode
    if e.name == '1' and current_mode == MODE.CHOSING:
        current_mode = MODE.AUTO_ACCEPT
    if e.name == '2' and current_mode == MODE.CHOSING:
        current_mode = MODE.AUTO_START
    if e.name == 'esc' and current_mode != MODE.CHOSING:
        current_mode = MODE.CHOSING
    if e.name == '3' and current_mode == MODE.CHOSING:
        current_mode = MODE.QUIT

keyboard.on_press(on_press)

if(__name__=='__main__'):
    running = False
    try:
        init("config.json")
    except Exception as e:
        print(f"Error: {e}")
    player_list=[]
    while(current_mode != MODE.QUIT):
        if(current_mode == MODE.CHOSING):
            clear_screen()
            print_full_width("Chosing mode")
            print_full_width("1. Auto Accept           ",fill_char=' ')
            print_full_width("2. Auto Start(Quick Play)",fill_char=' ')
            print_full_width("3. Quit                  ",fill_char=' ')
            print_full_width("Press key to start")
            while(current_mode == MODE.CHOSING):
                time.sleep(0.1)
        ###else###
        try:
            
            im=capture_window("League of Legends")
            if(current_mode == MODE.AUTO_START):
                players=get_current_player(im,langPack)
                msg=get_chat_message(im,langPack)
                #刪除跟增加不在房間的玩家
                maintain_player_list(player_list,players)
                #更新玩家狀態
                update_plyer_list(player_list,msg)
                update_auto_start_terminal(player_list)
                #如果所有玩家都準備好了，則開始遊戲
                if(all(player['status'] == "ready" for player in player_list) and len(player_list) != 0):
                    touch("League of Legends",0.42,0.95)
                    current_mode = MODE.AUTO_ACCEPT
            if(current_mode == MODE.AUTO_ACCEPT):
                #UI
                waiting_for_accept()
                if(compare_image(get_ac_crop(im),ac_image)):
                    time.sleep(0.5)
                    touch("League of Legends",960/1920,820/1080)
                    current_mode = MODE.WAITING_ENTER_GAME
            if(current_mode == MODE.WAITING_ENTER_GAME):
                #如果有人拒絕進入遊戲，則回到自動接受模式
                clear_screen()
                print_full_width("Waiting for entering game")
                if(not compare_image(get_ac_crop(im),ac_image)):
                    current_mode = MODE.AUTO_ACCEPT
        except Exception as e:
            clear_screen()
            if("list index out of range" in str(e)):
                print_full_width("Error: Please start the game.")
            if("!_src.empty() in function 'cv::cvtColor'" in str(e)):
                print_full_width("Error: Please make sure the image(ac_crop_1.png) is not empty.")
            else:
                print_full_width(f"Error: {e}")
            time.sleep(5)
            current_mode = MODE.CHOSING
    clear_screen()
    print_full_width("The program is terminated.")
    time.sleep(0.5)


