# LiveTranslator

LiveTranslator translates text from images using OCR and overlays the translated text directly on the images.

### Getting Started

#### Environments

- Install Dependencies: `pipenv install`
- Use virtual environment: `pipenv shell`
- Exit/Deactivate: `exit`

<!-- #### openai API
- generate openai API key from https://platform.openai.com/account/api-keys
- create a `key.txt` in root directory (make sure you are in root and do `touch key.txt`)
- paste your generated key into `key.txt` (this is meant for your own usage only, don't commit it) -->

#### Start

Use the following command to translate text from images:

```bash
python3 scripts/main.py translate --src <path_to_image> --print --print-boxes --from <lang> --to <lang>
```

#### Test

Use the following command to run tests:

```bash
python3 tests/run_tests.py
```

#### CLI Options Explanation

- --src (Required): Specify the path to the image file to be translated.
- --print (Optional): Print extracted texts to the console.
- --print-boxes (Optional): Draw bounding boxes around the detected text in the image.
- --from (Optional): Specify the source language for OCR (e.g., "eng", "jpn"). If not specified, it's auto-detected.
- --to (Optional): Specify the target language for translation (default is "eng").
- --show (Optional): Show the final translated image.

#### Troubleshoot

- `pipenv --rm` + `pipenv --python 3.9` + reinstall dependencies
