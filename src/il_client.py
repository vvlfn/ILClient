"""
Import dependencies
"""

from difflib import SequenceMatcher
import os
from typing import Any, Union
import json
import time
import keyboard  # type: ignore
import numpy as np
import numpy.typing as npt
import pyperclip  # type: ignore
from globals import SETTINGS_PATH
# mypy stubs :c
from pyautogui import hotkey, press, typewrite, position, click  # type: ignore


class ILClient:
    def __init__(
        self,  data_path: str, config: bool = False
    ) -> None:
        with open(SETTINGS_PATH) as f:
            settings: dict[str, Any] = json.load(f)
        self.data_path: str = data_path
        if not os.path.isfile(self.data_path):
            with open(self.data_path, "w") as f:
                json.dump({}, f, indent=2)

        # self.question_height = settings.get("question_height", 200)
        # self.answer_height = settings.get("answer_height", 300)
        self.sentence_coordiantes: tuple[int, int] = tuple(
            settings.get("sentence_coordinates", [100, 200])
        )
        self.answer_coordinates: tuple[int, int] = tuple(
            settings.get("answer_coordinates", [100, 300])
        )
        self.sentence_input_coordinates: tuple[int, int] = tuple(
            settings.get("sentence_input_coordinates", [500, 500])
        )
        self.login: str = settings.get("login", "")
        self.password: str = settings.get("password", "")

        # keybinds
        self.get_answer_key: str = settings.get("get_answer_key", "=")
        self.exit_key: str = settings.get("exit_key", "esc")

        # delays
        self.enter_delay: float = settings.get("enter_delay", 0.3)
        self.call_delay: float = settings.get("call_delay", 0.05)
        if config:
            self.SetCoordinates()

    def SetCoordinates(self) -> None:
        def InputCoordinates(message: str) -> tuple[int, int]:
            """Get coordinates from user input"""
            print(message)
            entered: bool = False
            while not entered:
                if keyboard.is_pressed("="):
                    coordinates = tuple(position())
                    print(f"Question coordinates saved: {coordinates}")
                    entered = True
                    break
            time.sleep(0.5)
            return coordinates
        # TODO: hover over specific place and press key '=' to save coordinates
        self.sentence_coordiantes = InputCoordinates(
            "Hover over the question and press `=`")
        self.sentence_input_coordinates = InputCoordinates(
            "Hover over the sentence input and press `=`")
        self.answer_coordinates = InputCoordinates(
            "Hover over the answer and press `=`")
        with open(SETTINGS_PATH, "r") as f:
            settings: dict[str, Any] = json.load(f)
            settings.update({"sentence_coordinates": self.sentence_coordiantes,
                            "sentence_input_coordinates": self.sentence_input_coordinates,
                             "answer_coordinates": self.answer_coordinates})
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=2)

    def __call__(self) -> None:
        """Get question by triple clicking the line and saves it, then gets answer from that inputs"""
        question: str = self.ClickCopy(self.sentence_coordiantes)
        with open(self.data_path, "r") as f:
            data: dict[str, str] = json.load(f)
        answer: str = data.get(question, "")
        click(*self.sentence_input_coordinates)
        if answer != "":
            typewrite(answer)
            press("enter")
            time.sleep(self.enter_delay)
            press("enter")
        else:
            press("enter")
            new_answer: str = self.ClickCopy(self.answer_coordinates)
            if not new_answer[:21:] == "Teraz bez dodatkowego":
                self.UpdateDataFile({question: new_answer})
            press("enter")

    def AutoComplete(self) -> bool:
        # from the main page get to the actual excercise page
        while self.ClickCopy(self.sentence_coordiantes)[:10:] != "Gratulacje":
            if keyboard.is_pressed("esc"):
                print("Exiting autocompleting.")
                return False
            self.__call__()
            time.sleep(self.call_delay)
        else:
            press("enter")
            return True

    def ClickCopy(self, coordinates: tuple[int, int], amount: int = 3) -> str:
        click(*coordinates, amount)
        hotkey("ctrl", "c")
        output: str = pyperclip.paste().strip()
        return output

    def UpdateDataFile(self, new_data: dict[str, str]) -> None:
        """Insert the updated data dictionary into the data.json file

        Args:
            data (dict[str, str]): dictionary of questions and answers
        """
        with open(self.data_path, "r") as f:
            data: dict[str, str] = json.load(f)
            data.update(new_data)
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    pass
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
