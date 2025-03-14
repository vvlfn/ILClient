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

# mypy stubs :c
from pyautogui import hotkey, press, typewrite, position, click  # type: ignore


class ILClient:
    def __init__(
        self, settings: dict[str, Any], data_path: str, config: bool = False
    ) -> None:
        self.data_path: str = data_path
        if not os.path.isfile(self.data_path):
            with open(self.data_path, "w") as f:
                json.dump({}, f, indent=2)

        # self.question_height = settings.get("question_height", 200)
        # self.answer_height = settings.get("answer_height", 300)
        self.question_coordinates: tuple[int, int] = tuple(
            settings.get("question_coordinates", [100, 200])
        )
        self.answer_coordinates: tuple[int, int] = tuple(
            settings.get("answer_coordinates", [100, 300])
        )
        self.start_button_coordinates: tuple[int, int] = tuple(
            settings.get("start_button_coordinates", [500, 500])
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
        # TODO: hover over specific place and press key '=' to save coordinates
        print("Hover over the question input box and press '='")
        while True:
            if keyboard.is_pressed("="):
                self.question_coordinates = tuple(position())
                print("Question coordinates saved!")
                break
        print("Hover over the answer input box and press '='")
        while True:
            if keyboard.is_pressed("="):
                self.answer_coordinates = tuple(position())
                print("Answer coordinates saved!")
                break
        # TODO: save coordinates to settings.json
        with open("settings.json", "r") as f:
            settings: dict[str, Any] = json.load(f)
        settings["question_coordinates"] = list(self.question_coordinates)
        settings["answer_coordinates"] = list(self.answer_coordinates)
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)

    def __call__(self) -> None:
        """Get question by triple clicking the line and saves it, then gets answer from that inputs"""
        question: str = self.TripleClick(self.question_coordinates)
        with open(self.data_path, "r") as f:
            data: dict[str, str] = json.load(f)
        answer: str = data.get(question, "")
        click(500, 500)
        if answer != "":
            typewrite(answer)
            press("enter")
            time.sleep(self.enter_delay)
            press("enter")
        else:
            press("enter")
            new_answer: str = self.TripleClick(self.answer_coordinates)
            if not new_answer[:21:] == "Teraz bez dodatkowego":
                self.UpdateDataFile({question: new_answer})
            press("enter")

    def AutoComplete(self) -> bool:
        # from the main page get to the actual excercise page
        while self.TripleClick(self.question_coordinates)[:10:] != "Gratulacje":
            if keyboard.is_pressed("esc"):
                print("Exiting autocompleting.")
                return False
            self.__call__()
            time.sleep(self.call_delay)
        else:
            press("enter")
            return True

    def TripleClick(self, coordinates: tuple[int, int]) -> str:
        click(*coordinates, 3)
        hotkey("ctrl", "c")
        output: str = pyperclip.paste().strip()
        return output

    def StartSession(self) -> int:
        # Open incognito new page, go to login screen, login and go to main screen
        time.sleep(0.3)
        # os.system('start https://')
        hotkey("ctrl", "shift", "n")
        typewrite("https://instaling.pl/teacher.php?page=login", 0)
        time.sleep(1)
        press("enter")
        time.sleep(2)
        typewrite(self.login)
        time.sleep(0.3)
        press("tab")
        time.sleep(0.3)
        typewrite(self.password)
        press("enter")
        time.sleep(1)
        # press tab 3 times and start session
        count: int = 0

        for i in range(4):
            press("tab", 3, 0.1)
            press("enter")
            time.sleep(0.7)
            click(*self.start_button_coordinates)
            time.sleep(0.3)
            uninterrupted: bool = self.AutoComplete()
            if uninterrupted:
                count += 1
            else:
                return count

        return count

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
