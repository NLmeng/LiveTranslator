# LiveTranslator
The goal of this project is to use AI to efficiently translate texts via OCR resposively in real time.

## GPT no API
This sub-project provides GPT-Plus subscribers the ability to use their GPT-4 in python without having access to GPT-4's API. It provides a function that substitute the actual API; it will essentially use https://chat.openai.com/chat in the background. This also supports the usage of older versions of GPT, this way you don't have to pay for the openai-API usage or wait for the API's waitlist.

### Getting Started

#### Environments
- Install Dependencies: `pipenv install`
- Use virtual environment: `pipenv shell`
- Exit/Deactivate: `exit`

#### openai API
- generate openai API key from https://platform.openai.com/account/api-keys
- create a `key.txt` in root directory (make sure you are in root and do `touch key.txt`)
- paste your generated key into `key.txt` (this is meant for your own usage only, don't commit it)

#### .env setup
- go to https://chat.openai.com/chat
- inspect the website
- go to application tab
- locate `Cookies` then locate the `https://chat.openai.com` tab under it
- copy the value of _puid (this is for `_PUID` in `.env`)
- go to network tab
- locate `Fetch/XHR`
- refresh the page and locate `models` then locate `authorization` under `Headers`
- copy the value of the `authorization` (don't copy Bearer) (this is for `OPENAI_API_KEY` in .env)

#### Start
- `python3 main.py`

#### Using GPT no API:
- `cd CustomGPT` (assuming you set up `.env` and launched `pipenv` like mentioned above)
- `python3 main.py`
