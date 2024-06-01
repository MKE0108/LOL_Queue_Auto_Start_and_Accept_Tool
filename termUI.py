import os
import sys
import time
import shutil
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
        print_full_width(f" Queue Waiting / number of player : {len(player_list)}  ")
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