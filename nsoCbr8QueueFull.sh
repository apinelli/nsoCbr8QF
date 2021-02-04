#!/bin/bash
source ~/ncsrun/scripts/nsoCbr8QueueFull/bin/activate
cd ~/ncsrun/scripts/nsoCbr8QueueFull
./nsoCbr8QueueFull.py
mv logs/*.* logs.old/

