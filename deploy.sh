#!/bin/bash

pip install --upgrade pip

virtualenv --python=/usr/bin/python3.10.7 my-env

source my-env/bin/activate

pip install -r requirements.txt
