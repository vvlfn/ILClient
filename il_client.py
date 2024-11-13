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
        self, settings: dict[str, Any], data_path: str, show_image: bool = False
    ) -> None:
        self.data_path: str = data_path
        self.show_image: bool = show_image

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
        # new answer box dimensions
        nax_start: int = settings.get("nax_start", 0)
        nay_start: int = settings.get("nay_start", 0)
        na_width: int = settings.get("na_width", 0)
        na_height: int = settings.get("na_height", 0)
        self.new_answer_bounding_box: tuple[int, int, int, int] = (
            nax_start,
            nay_start,
            nax_start + na_width,
            nay_start + na_height
        )

        # ocr config
        pytesseract.pytesseract.tesseract_cmd = settings["tesseract_cmd_path"]

        # keybinds
        self.get_answer_key: str = settings.get("get_answer_key", "=")
        self.exit_key: str = settings.get("exit_key", "esc")

        # delays
        self.enter_delay: float = settings.get("enter_delay", 0.3)

    def __call__(self) -> None:
        print("\n", "-"*15)
        question = self.RunOCR(self.answer_bounding_box)
        with open(self.data_path, "r") as f:
            data: dict[str, str] = json.load(f)
        answer: Union[str, None] = self.GetAnswer(question, data)
        print(f"{answer=}")
        # Insert answer or update data
        if answer:
            # if answer insert it
            typewrite(answer)
            press("enter")
            time.sleep(self.enter_delay)
            press("enter")
        else:
            # if no answer for question, press enter and save the answer given
            press("enter")
            new_answer: str = self.RunOCR(self.new_answer_bounding_box)
            new_record: dict[str, str] = {question: new_answer}
            self.UpdateDataFile(new_record)
            press("enter")
        print("-"*15)

    def AutoComplete(self) -> None:
        while self.RunOCR(self.answer_bounding_box, False).split()[0][:10:] != "gratulacje":
            self.__call__()
            time.sleep(0.05)
        print("Finished a session!")
        press("enter")

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
        else:
            return None

    def RunOCR(self, bounding_box: tuple[int, int, int, int], print_result: bool = True) -> str:
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
        ocr_result = " ".join(ocr_result.strip().split())

        output: list[str] = ocr_result.split("\n")
        if print_result:
            print(f"ocr result='{''.join(output)}'")
        return output[0]

    def UpdateDataFile(self, data: dict[str, str]) -> None:
        """Insert the updated data dictionary into the data.json file

        Args:
            data (dict[str, str]): dictionary of questions and answers
        """
        with open(self.data_path, "r") as f:
            settings: dict[str, str] = json.load(f)
            settings.update(data)
        with open(self.data_path, "w") as f:
            json.dump(settings, f, indent=2)


if __name__ == "__main__":
    with open("settings.json") as f:
        settings: dict[str, Any] = json.load(f)
    il_client: ILClient = ILClient(settings, "data.json", show_image=True)
    response = il_client.RunOCR(il_client.answer_bounding_box).split()[0][:10:]
    print(response)
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
