# InstaLing Answers

![Instaling icon](https://instaling.pl/marketing/static/assets/InstaLing_face.svg)

## Installation

1. Run `setup.bat`
2. Run `run_config.bat` and press `\` in the correct spots
3. Done

## Usage

1. run `run.bat`
2. press `=` to start autocompleting
3. if something happens press `esc`  

## Dependencies

- [python](https://www.python.org/) (download manually, rest is downloaded automatically)
    - [numpy](https://pypi.org/project/numpy/)
    - [keyboard](https://pypi.org/project/keyboard/)
    - [pyautogui](https://pypi.org/project/PyAutoGUI/)

## Settings

- `start_button_coordinates` - `[x,y]` of the start button, change with `run_config.bat`
- `question_coordinates` - `[x,y]` of the question text, change with `run_config.bat`
- `answer_coordinates` - `[x,y]` of the answer box, change with `run_config.bat`
- `save_coordinates_key` - `\` by default
- `get_answer_key` - `=` by default
- `exit_key` - `esc` by default
- `enter_delay` - delay between enter inputs
- `call_delay` - delay between every complete of question
