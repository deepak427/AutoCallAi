#!/bin/bash

pip install --upgrade pip

pip install virtualenv

virtualenv --no-site-packages my-env

source my-env/bin/activate

pip install -r requirements.txt
