# LOL QUICKPLAY MODE Auto Start
# Demo Video
null



# Qucik start
Download [Release v1](https://github.com/MKE0108/LOL_QUICKPLAY_MODE_Auto_Start/releases )


# Edit and run code
## 1. Downlond python 3.10 and pip
ref: https://www.youtube.com/watch?v=FYkOr_7hOXw or Google or GPT ^_^

## 2. Download Tesseract & Set environment path  
ref : https://linuxhint.com/install-tesseract-windows/  
### Important
Choose the language pack you need. e.g. traditional Chinese  
![](https://github.com/MKE0108/LOL_NG_auto_Start/blob/main/readme/image1.jpg)  
if you don't choose traditional Chinese, you need to edit config.json.
```json
{
    "lang" : "chi_tra" <- edit here
}
```

## 3. Open powershell
```bash
cd C:\Users\user\Desktop
git clone git@github.com:MKE0108/LOL_QUICKPLAY_MODE_Auto_Start.git
cd C:\Users\user\Desktop\LOL_QUICKPLAY_MODE_Auto_Start #Your absolute path of this folder
pip install -r requirement.txt
python run.py # or python3 run.py
```
Then you will find a new folder in your Desktop　^_^
