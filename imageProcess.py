import numpy as np
import pytesseract
from skimage.metrics import structural_similarity as ssim    
from cv2 import cvtColor, COLOR_BGR2GRAY, threshold, THRESH_BINARY, resize, imread

def get_ac_crop(img:np.array):
    y=130/1080
    x=550/1920
    w=820/1920
    h=840/1080
    return img[int(y*img.shape[0]):int((y+h)*img.shape[0]),int(x*img.shape[1]):int((x+w)*img.shape[1])]

#get current player
def get_current_player(img:np.array,langPack="chi_tra"):
    img = cvtColor(img, COLOR_BGR2GRAY)

    _,img = threshold(img,170, 255, THRESH_BINARY)

    #find current player
    players = []
    positions = [[655/1920,515/1080,275/1920,45/1080],
                    [370/1920,490/1080,275/1920,45/1080],
                    [(370+(370-675))/1920,490/1080,275/1920,45/1080],
                    [962/1920,490/1080,275/1920,45/1080],
                    [(962+(962-665))/1920,490/1080,275/1920,45/1080],
                    ]
    for p in positions:
        x,y,w,h = p
        cropped=img[int(y*img.shape[0]):int((y+h)*img.shape[0]),int(x*img.shape[1]):int((x+w)*img.shape[1])]
        text = pytesseract.image_to_string(cropped,lang=langPack)
        player=[txt.strip() for txt in text.split("\n") if len(txt.strip())!=0]
        if(len(player)!=0):
            players.append(player[0])
    return players

def get_chat_message(screenshot:np.array,langPack="chi_tra"):
    #chat area
    left = 0
    top = screenshot.shape[0] - screenshot.shape[0] // 5.3
    right = int(screenshot.shape[1] / 4)
    bottom = screenshot.shape[0]*9.2//10

    cropped_image = screenshot[int(top):int(bottom),int(left):int(right)]
    cropped_image=cvtColor(cropped_image, COLOR_BGR2GRAY)
    # pytesseract OCR
    text = pytesseract.image_to_string(cropped_image,lang=langPack,config='--psm 6')
    line=[txt.strip() for txt in text.split("\n") if len(txt.strip())!=0]
    return line
#compare two image
def compare_image(img1:np.array,img2:np.array,threshold=0.5,size=(100,100)):
    img1 = cvtColor(img1, COLOR_BGR2GRAY)
    img2 = cvtColor(img2, COLOR_BGR2GRAY)
    img1 = resize(img1, size)
    img2 = resize(img2, size)
    return ssim(img1,img2,full=True)[0]>=threshold