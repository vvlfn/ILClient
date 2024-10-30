import json
import os
import sys
from typing import Union
from PIL import ImageGrab
from PIL import Image
import numpy as np
import pytesseract
import pyperclip
from pyautogui import typewrite, press
import keyboard
x_start, y_start = 750, 200
x_size, y_size = 450, 100
pytesseract.pytesseract.tesseract_cmd = os.path.join(
    ".", "tesseract", "tesseract.exe")


def GetOCR() -> str:
    screenshot = ImageGrab.grab()
    # img1 = img.crop((672, 200, 600, 50))
    img_cropped = screenshot.crop(
        (x_start, y_start, x_start+x_size, y_start+y_size))
    img_arr = np.array(img_cropped)
    ocr_res: str = pytesseract.image_to_string(img_arr)
    ocr_res = ocr_res.lower()
    data = ocr_res.split("\n", 1)[0]
    return data


def InsertAnswer() -> None:
    press('backspace')
    question: str = GetOCR()
    with open("data.json") as f:
        data: dict[str, str] = json.load(f)

    answer: Union[str, None] = data.get(question)
    if answer is None:
        new_answer: str = input(f"Input answer for the question {question} ")
        data.update({question: new_answer})
        with open("data.json", "w") as f:
            json.dump(data, f)
    else:
        typewrite(answer)


def Main():
    while True:
        if keyboard.is_pressed("="):
            InsertAnswer()
        elif keyboard.is_pressed("esc"):
            sys.exit()


if __name__ == "__main__":
    Main()
