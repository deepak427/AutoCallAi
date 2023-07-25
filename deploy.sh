#!/bin/bash

C:/Python/python.exe -m pip install --upgrade pip

pip install -r requirements.txt

waitress-serve --port=5126 app:app