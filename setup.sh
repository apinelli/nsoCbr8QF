#!/bin/bash
python3 -m venv .
source bin/activate
pip install configparser
mkdir logs
mkdir logs.old
