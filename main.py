import json
import sys
from typing import Any, Union
from PIL import ImageGrab
from PIL.Image import Image
import numpy as np
import numpy.typing as npt
# mypy stubs :c
import pytesseract  # type: ignore
from pyautogui import typewrite, press
import keyboard


# SETTINGS
with open("settings.json") as f:
    settings = json.load(f)

x_start, y_start = settings["x_start"], settings["y_start"]
width, height = settings["width"], settings["height"]
try:
    pytesseract.pytesseract.tesseract_cmd = settings["tesseract_cmd_path"]
except pytesseract.TesseractNotFoundError as e:
    sys.exit(f"{e}, {settings["tesseract_cmd_path"]}")
except FileNotFoundError as e:
    sys.exit(f"{e}, {settings["tesseract_cmd_path"]}")
get_answer_key = settings["get_answer_key"]
exit_key = settings["exit_key"]


def GetOCR() -> str:
    """_summary_

    Returns:
        str: _string of the question_
    """
    screenshot: Image = ImageGrab.grab()
    img_cropped: Image = screenshot.crop(
        (x_start, y_start, x_start+width, y_start+height))
    img_arr: npt.ArrayLike = np.array(img_cropped)
    ocr_res: str = pytesseract.image_to_string(img_arr)
    ocr_res = ocr_res.lower()
    data: str = ocr_res.split("\n", 1)[0]
    return data


def InsertAnswer() -> None:
    """_summary_
    On key press removes the answer key (presses backspace) and reads the answer from data.json file.
    If there is no answer recorder asks to input through the terminal, if it exists simulates typing it into the text box
    """
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
    print(settings["tesseract_cmd_path"])
    while True:
        if keyboard.is_pressed(get_answer_key):
            InsertAnswer()
        elif keyboard.is_pressed(exit_key):
            sys.exit()


if __name__ == "__main__":
    Main()
