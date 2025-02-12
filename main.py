"""
Import dependencies
"""

from typing import Any, Union
import json
import os
import sys
import time
import argparse
import keyboard  # type: ignore
import numpy as np
import numpy.typing as npt

# mypy stubs :c=
from pyautogui import typewrite, press  # type: ignore

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
    parser.add_argument("-config", "--set_coordinates",
                        help="Set coordinates of mouse clicks", action="store_true")
    args = parser.parse_args()

    il_client: ILClient = ILClient(
        settings, os.path.join("data.json"), config=args.set_coordinates
    )

    print(
        f"Program ready, complete a session by pressing `{
            execute_key}` or exit the program by pressing `{exit_key}`"
    )
    """
    
    Main Loop
    """

    while True:
        if keyboard.is_pressed(execute_key):
            # remove keybind key in text box
            press("backspace")
            # il_client()
            il_client.AutoComplete()
        elif keyboard.is_pressed("\\"):
            il_client.StartSession()
        elif keyboard.is_pressed(exit_key):
            sys.exit(0)


if __name__ == "__main__":
    print(
        """
██▒   █▓ ██▒   █▓ ██▓      █████▒███▄    █ 
▓██░   █▒▓██░   █▒▓██▒    ▓██   ▒ ██ ▀█   █ 
 ▓██  █▒░ ▓██  █▒░▒██░    ▒████ ░▓██  ▀█ ██▒
  ▒██ █░░  ▒██ █░░▒██░    ░▓█▒  ░▓██▒  ▐▌██▒
   ▒▀█░     ▒▀█░  ░██████▒░▒█░   ▒██░   ▓██░
   ░ ▐░     ░ ▐░  ░ ▒░▓  ░ ▒ ░   ░ ▒░   ▒ ▒ 
   ░ ░░     ░ ░░  ░ ░ ▒  ░ ░     ░ ░░   ░ ▒░
     ░░       ░░    ░ ░    ░ ░      ░   ░ ░ 
      ░        ░      ░  ░                ░ 
     ░        ░                             """
    )
    Main()
