#!/bin/bash

pip install --upgrade pip

pip install virtualenv

virtualenv --python=/usr/bin/python3.10.7 my-env

source my-env/bin/activate

pip install -r requirements.txt
