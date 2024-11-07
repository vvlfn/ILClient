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


class ILClient:
    def __init__(self, settings: dict[str, Any], data_path: os.PathLike, show_image: bool = False) -> None:
        self.data_path: os.PathLike = data_path
        # LOAD VARIABLES

        # answer box dimensions
        abx_start: int = settings.get("abx_start", 0)
        aby_start: int = settings.get("aby_start", 175)
        ab_width: int = settings.get("ab_width", 1920)
        ab_height: int = settings.get("ab_height", 100)
        self.answer_bounding_box: tuple[int, int, int, int] = (
            abx_start, aby_start, abx_start+ab_width, aby_start+ab_height)

        # ocr config
        pytesseract.pytesseract.tesseract_cmd = settings["tesseract_cmd_path"]

        # keybinds
        self.get_answer_key: str = settings.get("get_answer_key", "=")
        self.exit_key: str = settings.get("exit_key", "esc")

        # delays
        self.enter_delay: float = settings.get("enter_delay", 0.3)

        # args from parser
        self.show_image: bool = show_image

    def __call__(self) -> None:
        # remove keybind key in text box
        press('backspace')

        question = self.RunOCR(self.answer_bounding_box)
        # load data
        with open(self.data_path, "r") as f:
            data: dict[str, str] = json.load(f)

        answer: Union[str, None] = ""
        # TODO

    def RunOCR(self, bounding_box: tuple[int, int, int, int]) -> Any:
        """Takes a screenshot, crops it and runs OCR on it.
        Args:
            bounding_box (tuple[int, int, int, int]): Bounding Box of the ocr image (x_start, y_start, width, height)

        Returns:
            Any: The OCR result
        """
        screenshot: Image = ImageGrab.grab()
        cropped_screenshot: Image = screenshot.crop(bounding_box)

        # if argument -img inserted then show image
        if self.show_image:
            cropped_screenshot.show("Cropped Screenshot")

        # Image -> numpy array
        ocr_data: npt.ArrayLike = np.array(cropped_screenshot)
        # get ocr string and turn it lowercase
        ocr_result: str = pytesseract.image_to_string(
            ocr_data, lang="eng").lower()
        # replace underscores
        ocr_result = ocr_result.replace("_", " ")
        # remove multi whitespace, multiple spaces next to eachother
        ocr_result = ' '.join(ocr_result.strip().split())

        output = ocr_result.split("\n")

    def InsertAnswer(self, answer: str) -> None:
        """Types in the string provided and presses enter twice with a delay between
        Args:
            answer (str): Answer string to simulate typing
        """
        typewrite(answer)

        press("enter")
        time.sleep(self.enter_delay)
        press("enter")

    def UpdateDataFile(self, data: dict[str, str]) -> None:
        """Insert the updated data dictionary into the data.json file

        Args:
            data (dict[str, str]): dictionary of questions and answers
        """
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=2)
