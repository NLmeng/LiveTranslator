# LiveTranslator

LiveTranslator finds and translates texts from images within the region or window using OCR and overlays the translated texts.

### Getting Started

#### Requirements

- Python, Pip, Pipenv

### Setup Instructions

1. **Clone the repository**:

   ```sh
   git clone <repository-url>
   cd LiveTranslator
   ```

2. **Run the environment setup script**:

   ```sh
   python setup_env.py
   ```

3. **Install the dependencies**:

   ```sh
   pipenv install
   ```

4. **Use the virtual environment**:

   ```sh
   pipenv shell
   ```

5. **Exit/Deactivate the virtual environment**:
   ```sh
   exit
   ```

### Usage

#### Translate Text from Images

Use the following command to translate text from images:

```sh
python3 scripts/main.py translate --src <path_to_image> --print --print-boxes --from <lang> --to <lang> --translator <translator>
```

##### CLI Options Explanation

- `--src` (Required): Specify the path to the image file to be translated.
- `--print` (Optional): Print extracted texts to the console.
- `--print-boxes` (Optional): Draw bounding boxes around the detected text in the image.
- `--from` (Optional): Specify the source language for OCR (e.g., "eng", "jpn"). If not specified, it's auto-detected.
- `--to` (Optional): Specify the target language for translation (default is "eng").
- `--show` (Optional): Show the final translated image.
- `--translator` (Optional): Choose the translation service (default is "google"). Options: `google`, `deepl`.

#### Run the GUI

Use the following command to run the application's GUI:

```sh
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

### Testing

Use the following command to run tests:

```sh
python3 tests/run_tests.py <modules>
```

##### CLI Options Explanation

- `modules` (Optional): Paths to specific test modules or classes. **Leaving empty will run all tests**
- `-v, --verbosity` (Optional): Verbosity level for test output.
  - 0: Minimal output
  - 1: Normal output (default)
  - 2: Detailed output
  - 3: Debug-level output
- `--failfast` (Optional): Stop running tests on the first failure.
- `--buffer` (Optional): Buffer stdout and stderr during test execution.

### Troubleshooting

- If you encounter issues, you can remove the virtual environment and reinstall dependencies:
  ```sh
  pipenv --rm
  pipenv --python 3.9
  pipenv install
  ```

### Example Usage

To translate text from an image using the Google Translator, run:

```sh
python3 scripts/main.py translate --src path/to/your/image.png --print --print-boxes --from eng --to jpn --translator google --show
```

### Running the Application

To run the application GUI, use:

```sh
python3 scripts/main.py gui
```
