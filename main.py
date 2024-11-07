from difflib import SequenceMatcher
import json
import os
import sys
import time
from typing import Any, Union
from PIL import ImageGrab
from PIL.Image import Image
import numpy as np
import numpy.typing as npt
# mypy stubs :c
import pytesseract  # type: ignore
from pyautogui import typewrite, press
import pyautogui
import keyboard
import argparse
import random

# SETTINGS
with open("settings.json") as f:
    settings: dict[str, Any] = json.load(f)

x_start, y_start = settings.get("x_start", 0), settings.get("y_start", 175)
width, height = settings.get("width", 1920), settings.get("height", 100)
try:
    pytesseract.pytesseract.tesseract_cmd = settings["tesseract_cmd_path"]
except pytesseract.TesseractNotFoundError as e:
    sys.exit(f"{e}, {settings.get(
        "tesseract_cmd_path", ".\\tesseract\\tesseract.exe")}")
except FileNotFoundError as e:
    sys.exit(f"{e}, {settings["tesseract_cmd_path"]}")
get_answer_key: str = settings.get("get_answer_key", "=")
exit_key: str = settings.get("exit_key", "esc")
enter_delay: int = settings.get("enter_delay", 0.3)
base_delay: float = settings.get("typing_base_delay", 0.01)
lower_multiplier: int = settings.get("typing_lower_multiplier", 1)
upper_multiplier: int = settings.get("typing_upper_multiplier", 4)


def GetOCR() -> str:
    """_summary_

    Returns:
        str: _string of the question_
    """
    screenshot: Image = ImageGrab.grab()
    img_cropped: Image = screenshot.crop(
        (x_start, y_start, x_start+width, y_start+height))
    if args.show_image:
        img_cropped.show()
    img_arr: npt.ArrayLike = np.array(img_cropped)
    ocr_res: str = pytesseract.image_to_string(img_arr, lang="eng")
    ocr_res = ocr_res.lower()
    data: str = ocr_res.split("\n", 1)[0]
    return data


def InsertAnswer() -> None:
    """_summary_
    On key press removes the answer key (presses backspace) and reads the answer from data.json file.
    If there is no answer recorder asks to input through the terminal, if it exists simulates typing it into the text box
    """
    press('backspace')
    # question: str  GetOCR()
    ocr_res: str = GetOCR()
    question: str = ' '.join(ocr_res.replace("_", " ").strip().split())
    with open("data.json") as f:
        data: dict[str, str] = json.load(f)
        answer: Union[str, None] = ""
    for key in data.keys():
        similarity: float = SequenceMatcher(None, key, question).ratio()
        if similarity >= 0.975:
            answer = data.get(key, None)
            try:
                EnterAnswer(answer)  # type: ignore
            except TypeError as e:
                print(f"{answer=} | {e}")
            return None
        elif similarity >= 0.75:
            print(round(similarity, 2), key, question, sep="\n")
            answer = data.get(key)
            choice: str = input("Change 1st key to 2nd key? y/N")
            if choice.lower() == "y":
                data.update({question: answer})  # type: ignore
                data.pop(key)
                UpdateDataJSON(data)
                print(answer)
                return None
            break
        else:
            answer = data.get(question)
    print(f"{answer=}")
    if answer is None:
        new_answer: str = input(f"Input answer for the question {
                                question.strip("\n")} ")
        if new_answer == "":
            return None
        data.update({question: new_answer})
        UpdateDataJSON(data)
    else:
        EnterAnswer(answer)


def EnterAnswer(answer: str):
    for letter in answer:
        pyautogui.PAUSE = 0.01 * random.randint(1, 4)
        press(letter)

    press("enter")
    time.sleep(enter_delay)
    press("enter")


def UpdateDataJSON(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)


def Main():
    if not os.path.isfile("data.json"):
        open("data.json", "w").close()
    while True:
        if keyboard.is_pressed(get_answer_key):
            InsertAnswer()
        elif keyboard.is_pressed(exit_key):
            sys.exit()


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-img", "--show_image",
                        help="Show cropped image from screenshot", action="store_true")
    args = parser.parse_args()
    # is_debug: bool = bool(sys.argv[1])
    Main()
