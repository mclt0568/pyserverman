#!/usr/bin/bash

python3 main.py
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf