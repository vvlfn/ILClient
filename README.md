# InstaLing Answers

## Installation

1. Run `setup.bat`
2. Install the latest release of tesseract
3. Install tesseract into the repo directory (path will be like `<path to this dir>\tesseract`)

## Usage

1. run `run.bat`
2. press `=` by default
3. :)
4. if something happens press `esc` by default

## Dependencies

- tesseract ([python](https://pypi.org/project/pytesseract/) + [tool](https://github.com/UB-Mannheim/tesseract/wiki))
- [pillow](https://pypi.org/project/pillow/)
- [numpy](https://pypi.org/project/numpy/)
- [keyboard](https://pypi.org/project/keyboard/)
- [pyautogui](https://pypi.org/project/PyAutoGUI/)

## Settings

- `'tesseract_cmd_path'` - relative/absolute path to tesseract.exe file
- `'abx_start'` - (ab = answer box) distance from the left side of the screen to the answer box
- `'aby_start'` - (ab = answer box) distance from the top of the screen to the answer box
- `'ab_width'` - (ab = answer box) width of the answer box
- `'ab_height'` - (ab = answer box) height of the answer box
- `an_x ...` - (answer) the same 4 parameters as with the answer box
- `end_x ...` - (end) the same 4 parameters as with the answer box
- `'get_answer_key'` - key to get answer and type it in
- `'exit_key'` - key to close the program
- `'enter_delay'` - delay between first and second enter press
- `'typing_base_delay'` - typing base delay between letter presses
- `'typing_lower_multiplier'` - typing multiplier lower bound
- `'typing_upper_multiplier'` - typing multiplier upper bound
