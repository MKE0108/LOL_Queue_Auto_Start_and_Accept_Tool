# LOL QUICKPLAY MODE Auto Start
# Demo Video

# Quick start
## 1. Open powershell
```bash
cd C:\Users\user\Desktop
git clone git@github.com:MKE0108/LOL_QUICKPLAY_MODE_Auto_Start.git
```
Then you will find a new folder in your Desktop　^_^
## 2. Downlond python 3.10
## 3. Enter in powershell
```bash
cd C:\Users\user\Desktop\LOL_QUICKPLAY_MODE_Auto_Start #Your absolute path of this folder
```
## 4. Enter in powershell
```bash
pip install -r requirement.txt
```

## 5. Download Tesseract & Set environment path  
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

## 6. Press this in powershell
```bash
python run.py # or python3 run.py
```
