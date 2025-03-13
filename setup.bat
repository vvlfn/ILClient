cd /D "%~dp0"
if not exist .venv\ (
    py -m venv .venv
)
.venv\Scripts\activate.bat && py -m pip install pillow numpy keyboard pyautogui colorama