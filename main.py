"""
Import dependencies
"""

from difflib import SequenceMatcher
from typing import Any, Union
import json
import os
import sys
import time
import argparse
from PIL import ImageGrab
from PIL.Image import Image
import keyboard
import numpy as np
import numpy.typing as npt

# mypy stubs :c
import pytesseract  # type: ignore
from pyautogui import typewrite, press

from il_client import ILClient


# TODO
# *- skip new words
# *- insert answers auitomatically

def Main() -> None:
    """
    Load Settings
    """
    with open("settings.json") as f:
        settings: dict[str, Any] = json.load(f)

    execute_key: str = settings.get("get_answer_key", "=")
    exit_key: str = settings.get("exit_key", "esc")

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-img",
        "--show_image",
        help="Show cropped image from screenshot",
        action="store_true",
    )
    args = parser.parse_args()
    il_client: ILClient = ILClient(settings, os.path.join(
        "data.json"), show_image=args.show_image)

    """
    Main Loop
    """

    while True:
        if keyboard.is_pressed(execute_key):
            # il_client()
            il_client.AutoComplete()
        elif keyboard.is_pressed(exit_key):
            sys.exit(0)


if __name__ == "__main__":
    Main()
