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
from colorama import init as crInit, Fore, Back, Style  # type: ignore
# mypy stubs :c=
from pyautogui import typewrite, press  # type: ignore
from globals import SETTINGS_PATH

from il_client import ILClient
from date_handler import DateHandler


def PrintHeader(dh: DateHandler, execute_key: str = "=", exit_key: str = "esc", session_finished: bool = False) -> None:
    try:
        if dh.ReadDate()[1] == 0:
            color = Fore.RED
        elif dh.ReadDate()[1] >= 4:
            color = Fore.CYAN + Style.BRIGHT
        else:
            color = Fore.GREEN
    except KeyError:
        color = Fore.RED

    try:
        if dh.ReadDate(dh.last_date)[1] == 0:
            color_last = Fore.RED
        elif dh.ReadDate(dh.last_date)[1] >= 4:
            color_last = Fore.YELLOW + Style.BRIGHT
        else:
            color_last = Fore.MAGENTA
    except KeyError:
        color_last = Fore.RED
    os.system("cls")
    print(Fore.MAGENTA + Style.BRIGHT +
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
     ░        ░                             """ + Style.RESET_ALL
          )
    print(
        f"{Style.BRIGHT}Program ready{Style.RESET_ALL}, complete a session by pressing `{
            execute_key}` or exit the program by pressing `{exit_key}`"
    )

    print(
        f"Last session finished on: {Style.BRIGHT + color_last + dh.last_date + Style.RESET_ALL} with {Style.BRIGHT + color_last + str(dh.ReadDate(dh.last_date)[1]) + Style.RESET_ALL} sessions"
    )
    print(
        f"Current date: {Style.BRIGHT + color + dh.current_date + Style.RESET_ALL} with {Style.BRIGHT + color + str(dh.ReadDate()[1]) + Style.RESET_ALL} sessions"
    )

    if session_finished:
        print("Session finished!")


def Main() -> None:
    """
    Load Settings
    """
    crInit()
    with open(SETTINGS_PATH) as f:
        settings: dict[str, Any] = json.load(f)

    execute_key: str = settings.get("get_answer_key", "=")
    exit_key: str = settings.get("exit_key", "esc")

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-config",
        "--set_coordinates",
        help="Set coordinates of mouse clicks",
        action="store_true",
    )
    args = parser.parse_args()

    il_client: ILClient = ILClient(
        os.path.join("./data/data.json"), config=args.set_coordinates
    )

    dh: DateHandler = DateHandler()

    """
    Main Loop
    """

    PrintHeader(dh, execute_key=execute_key, exit_key=exit_key)

    while True:
        if keyboard.is_pressed(execute_key):
            # remove keybind key in text box
            press("backspace")
            uninterrupted: bool = il_client.AutoComplete()
            if uninterrupted:
                dh.WriteToDate(dh.dates[dh.current_date] + 1)
                PrintHeader(dh, execute_key=execute_key,
                            exit_key=exit_key, session_finished=True)
        elif keyboard.is_pressed("\\"):
            il_client.StartSession()
        elif keyboard.is_pressed(exit_key):
            sys.exit(0)
        elif keyboard.is_pressed("r"):
            os.system(
                'start https://instaling.pl/student/pages/mainPage.php?student_id=2558385')

            time.sleep(0.5)


if __name__ == "__main__":
    Main()
    # datehandler = DateHandler()
