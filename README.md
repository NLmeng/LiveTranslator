# LiveTranslator

LiveTranslator translates text from images using OCR and overlays the translated text directly on the images.

### Getting Started

#### Requirements

- Python, Pip, Pipenv

#### Environments

- Install Dependencies: `python setup_env.py pipenv install`
- Use virtual environment: `pipenv shell`
- Exit/Deactivate: `exit`

#### Start

Use the following command to translate text from images:

```bash
python3 scripts/main.py translate --src <path_to_image> --print --print-boxes --from <lang> --to <lang> --translator <translator>
```

#### CLI Options Explanation

- `--src` (Required): Specify the path to the image file to be translated.
- `--print` (Optional): Print extracted texts to the console.
- `--print-boxes` (Optional): Draw bounding boxes around the detected text in the image.
- `--from` (Optional): Specify the source language for OCR (e.g., "eng", "jpn"). If not specified, it's auto-detected.
- `--to` (Optional): Specify the target language for translation (default is "eng").
- `--show` (Optional): Show the final translated image.
- `--translator` (Optional): Choose the translation service (default is "google"). Options: `google`, `deepl`.

Use the following command to run the application's GUI:

```bash
python3 scripts/main.py gui
```

### GUI Features

The LiveTranslator GUI allows users to capture and translate text from specific windows or regions of their screen. The main features include:

1. **Select Capture Mode**:

   - `Capture in Intervals`: Capture the selected window/region at regular intervals.
   - `Capture and Wait`: Capture the selected window/region once and wait until the translated window is closed.

2. **Set Capture Interval**:

   - Set the interval (in seconds) for capturing the screen in `Capture in Intervals` mode.

3. **Select Source and Target Languages**:

   - Choose from supported languages (e.g., English, Japanese, French) for OCR and translation.

4. **Select Capture Type**:

   - `Window`: Capture a specific window.
   - `Region`: Capture a user-defined region of the screen.

5. **Window List**:

   - Refresh and select from a list of currently open windows for capturing.

6. **Region Selection**:

   - Manually select a region of the screen for capturing and translation.

7. **Start and Stop Capture**:

   - Start capturing the selected window/region and translating the text.
   - Stop the capture process.

8. **Status Display**:
   - A status label displays the current state of the capture process, with tooltips for additional information.

### Test

Use the following command to run tests:

```bash
python3 tests/run_tests.py <modules>
```

#### CLI Options Explanation

- `modules` (Optional): Paths to specific test modules or classes. **Leaving empty will run all tests**
- `-v, --verbosity` (Optional): Verbosity level for test output.
  - 0: Minimal output
  - 1: Normal output (default)
  - 2: Detailed output
  - 3: Debug-level output
- `--failfast` (Optional): Stop running tests on the first failure.
- `--buffer` (Optional): Buffer stdout and stderr during test execution.

### Troubleshoot

- `pipenv --rm` + `pipenv --python 3.9` + reinstall dependencies

### Example Usage

To translate text from an image using the Google Translator, run:

```bash
python3 scripts/main.py translate --src path/to/your/image.png --print --print-boxes --from eng --to jpn --translator google --show
```

## To run the application

```bash
python3 scripts/main.py gui
```
