# Pattern Matching & Replacement

This is a web application using Django and React that allows users
to upload CSV or Excel files, identify patterns in text columns using natural language
input, and replace the matched patterns.

## Requirements

- Python 3.12+
- Nodejs 20+

## Installation

Create a virtual environment.
`python -m venv .venv`

Activate the virtual environment.
For Windows:

- In cmd.exe
  `.venv\Scripts\activate.bat`

- In PowerShell
  `.venv\Scripts\Activate.ps1`

For Linux and MacOS:
`source .venv/bin/activate`

Install the required python packages.
`pip install -r requirements.txt`

Then install and build nodejs packages.
`npm install`
`npm run build`

Go to django project and do migration.
`cd llm_regex`
`python manage.py makemigrations`
`python manage.py migrate`

Now you can start the server.
`python manage.py runserver`

## Additional Note

This web application uses OpenAI as LLM and HuggingFace as embedding.

## Demo

[![IMAGE ALT TEXT HERE](https://raw.githubusercontent.com/wizdanmgs/llm-regex-pattern-matching-and-replacement/main/demo.png)](https://youtu.be/aWP4quONysU)
