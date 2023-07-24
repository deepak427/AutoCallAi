#!/bin/bash

pip install --upgrade pip

pip install -r requirements.txt

waitress-serve --port=5126 app:app