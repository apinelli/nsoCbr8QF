#!/bin/bash
source venv.sh
pip install configparser
./nsoCbr8QueueFull.py
mv logs/*.* logs.old/

