"""
Import dependencies
"""

from difflib import SequenceMatcher
from typing import Any, Union
import json
import os
import time
from PIL import ImageGrab
from PIL.Image import Image
import numpy as np
import numpy.typing as npt
import argparse

# mypy stubs :c
import pytesseract  # type: ignore
from pyautogui import typewrite, press


class ILClient:
    def __init__(
        self, settings: dict[str, Any], data_path: str, args: argparse.Namespace
    ) -> None:
        self.data_path: str = data_path
        self.args = args

        # answer box dimensions
        abx_start: int = settings.get("abx_start", 0)
        aby_start: int = settings.get("aby_start", 175)
        ab_width: int = settings.get("ab_width", 1920)
        ab_height: int = settings.get("ab_height", 100)
        self.answer_bounding_box: tuple[int, int, int, int] = (
            abx_start,
            aby_start,
            abx_start + ab_width,
            aby_start + ab_height,
        )

        # ocr config
        pytesseract.pytesseract.tesseract_cmd = settings["tesseract_cmd_path"]

        # keybinds
        self.get_answer_key: str = settings.get("get_answer_key", "=")
        self.exit_key: str = settings.get("exit_key", "esc")

        # delays
        self.enter_delay: float = settings.get("enter_delay", 0.3)

    def __call__(self) -> None:
        # remove keybind key in text box
        press("backspace")

        question = self.RunOCR(self.answer_bounding_box)
        with open(self.data_path, "r") as f:
            data: dict[str, str] = json.load(f)
        answer: Union[str, None] = self.GetAnswer(question, data)
        print(f"{answer=}")
        # Insert answer or update data
        if answer:
            self.InsertAnswer(answer)
        else:
            new_answer: str = input(
                f"Input answer for question {question=} \n Answer: "
            )
            if new_answer:
                data.update({question: answer})
                self.UpdateDataFile(data)

    def GetAnswer(self, question: str, data: dict[str, str]) -> str | None:
        # load data
        for key in data.keys():
            similarity: float = SequenceMatcher(None, key, question).ratio()
            if similarity >= 0.90:
                # ocr result is similar enough to existing -> get the existing key's answer and return
                answer = data.get(key, None)
                if answer:
                    return answer
            elif similarity <= 0.50:
                # there (most likely) is no similar question recorder -> get the ocr question's answer and return
                answer = data.get(question, None)
                if answer:
                    return answer

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
        if self.args.show_image:
            cropped_screenshot.show("Cropped Screenshot")

        # Image -> numpy array
        ocr_data: npt.ArrayLike = np.array(cropped_screenshot)
        # get ocr string and turn it lowercase
        ocr_result: str = pytesseract.image_to_string(ocr_data, lang="eng").lower()
        # replace underscores
        ocr_result = ocr_result.replace("_", " ")
        # remove multi whitespace, multiple spaces next to eachother
        ocr_result = " ".join(ocr_result.strip().split())

        output = ocr_result.split("\n")

        print(*output, "\n-")

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


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-img",
        "--show_image",
        help="Show cropped image from screenshot",
        action="store_true",
    )
    args = parser.parse_args()
    with open("settings.json") as f:
        settings: dict[str, Any] = json.load(f)
    il_client: ILClient = ILClient(settings, "data.json", args)
#          ___..._
#     _,--'       "`-.
#   ,'.  .            \
# ,/:. .     .       .'
# |;..  .      _..--'
# `--:...-,-'""\
#         |:.  `.
#         l;.   l
#         `|:.   |
#          |:.   `.,
#         .l;.    j, ,
#      `. \`;:.   //,/
#       .\\)`;,|\'/(
#        ` `itz `(,
