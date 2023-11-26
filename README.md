# LOL 快打模式 自動開始
## Quick start
1. open powershell
2. Downlond python 3.10
3. Press this in powershell
```bash
pip install -r requirement.txt
```
4. Press this in powershell
```bash
cd C:\Users\user\Documents\LOL_NG_auto_StartYour_Path #Your absolute path of this folder
```
5. Download Tesseract & Set environment path
ref : https://linuxhint.com/install-tesseract-windows/  
###Important
Choose the language pack you need. e.g. traditional Chinese
[](https://linuxhint.com/wp-content/uploads/2022/09/How-to-Install-Tesseract-on-Windows-8.png)  
if you don't choose traditional Chinese, you need to edit config.json.
```json
{
    "lang" : "cha-tra" <- edit here
}
```

6. Press this in powershell
```bash
python run.py # or python3 run.py
```