#!/bin/bash
python3 -m venv .
source venv.sh
sleep 5
pip install configparser
mkdir logs
mkdir logs.old
