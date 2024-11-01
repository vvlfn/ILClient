# InstaLing Answers

## Installation

1. Install tesseract tool from [this github repo](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installator and set the path to this directory with `\tesseract` at the end (optional but if different change `settings.json` `'tesseract_cmd_path'` value to path to tesseract.exe)
3. Set up virtual environment in this directory (folder name should be `.venv`)
4. Install dependencies with `pip install pillow numpy pytesseract pyautogui keyboard`
5. In cmd run `run.bat` file and then `py main.py -p` and adjust `x_start`, `y_start`, `width` and `height` to get only the text in the cropped img
6. run `py main.py` without any arguments and press the `get_answer_key` to input answers (if no answer is found input into the terminal)

## Dependencies

- tesseract ([python](https://pypi.org/project/pytesseract/) + [tool](https://github.com/UB-Mannheim/tesseract/wiki))
- [pillow](https://pypi.org/project/pillow/)
- [numpy](https://pypi.org/project/numpy/)
- [keyboard](https://pypi.org/project/keyboard/)
- [pyautogui](https://pypi.org/project/PyAutoGUI/)

## Settings

- `'tesseract_cmd_path'` - relative/absolute path to tesseract.exe file
- `'x_start'` - distance from the left side of the screen to the text box
- `'y_start'` - distance from the top of the screen to the text box
- `'width'` - width of the text box
- `'height'` - height of the text box
- `'get_answer_key'` - key to get answer and type it in
- `'exit_key'` - key to close the program
- `'enter_delay'` - delay between first and second enter press
- `'typing_base_delay'` - typing base delay between letter presses
- `'typing_lower_multiplier'` - typing multiplier lower bound
- `'typing_upper_multiplier'` - typing multiplier upper bound
