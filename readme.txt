------------------------------------------------------------------------------------------------
This script is intended to run in NSO servers connected to CBR8 devices. It will look for queue
stuck issues as described by CSCvw04657 and send e-mail alerts. 
It is suggested to add the script to a crontab service.
------------------------------------------------------------------------------------------------

1) Go to the folder you want to install (e.g. /home/user/ncsrun/scripts)

2) git clone https://github.com/apinelli/nsoCbr8QF.git

3) cd nsoCbr8QF

4) Update nsoCbr8QueueFull.ini file with sender's gmail address/password and recipient's e-mail addresses

5) Update inventory file with the CBR8 devices present in NSO database

6) ./setup.sh
- It will create a virtual environment for python 3 in the nsoCbr8QF folder
- It will enter the nsoCbr8QF folder
- It will create the "logs" and "logs.old" folders

7) Activate virtual environment:
$source bin/activate 

8) Install config parser:
$pip install configparser

9) Run python script:
./nsoCbr8QueueFull.py

