cd /D "%~dp0"
if not exists .venv\(
    py -m venv .venv
)
.venv\Scripts\activate.bat && py -m pip install pytesseract pillow numpy keyboard pyautogui
echo "A website will open. Download the newest release and install into this directory with the addition of `/tesseract` in the path"
pause
start https://github.com/UB-Mannheim/tesseract/releases/