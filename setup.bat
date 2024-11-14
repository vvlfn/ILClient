cd /D "%~dp0"
if not exist .venv\ (
    py -m venv .venv
)

@REM echo "A website will open. Download the newest release and install into this directory with the addition of `/tesseract` in the path"
@REM pause
@REM start https://github.com/UB-Mannheim/tesseract/releases/
curl -L -o installer.exe https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
installer.exe
.venv\Scripts\activate.bat && py -m pip install pytesseract pillow numpy keyboard pyautogui