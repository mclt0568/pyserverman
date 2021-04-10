#!/usr/bin/bash

python3 main.py -t
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf