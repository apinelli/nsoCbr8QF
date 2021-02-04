#!/bin/bash
python3 -m venv .
pip install configparser
source bin/activate
mkdir logs
mkdir logs.old
