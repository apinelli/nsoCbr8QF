===================================================================================================================
This script is intended to run in NSO servers connected to CBR8 devices. It will look for queue
stuck issues as described by CSCvw04657 and send e-mail alerts to authorized recipients, which allows faster service 
recovery by running a workaround (SUP switchover).
It is suggested to add the script to a crontab service.
===================================================================================================================

Background info:
----------------

1. What Is Stuck Queue?
When a queue to be deleted or moved cannot drain packets on it over a long period of time, it is "stuck". A "stuck queue" may block subsequent operations to setup CPP configurations for cable modem service flows etc. Some common symptoms are:
-- modems not online
-- modems online not pingable
-- WB modems use only primary for traffic, therefore cannot send more than 37Mbps traffic,

Below are some of possible reasons that could cause stuck queue:
 -- CLC constantly asserts XOFF
 -- link level back-pressure to Astro that prevents dequeue in CPP
 -- lack of credits in Astro
 -- software bugs in CPP client or cable application code

2. Check for Stuck Queues
for active SUP:
#show platform hardware qfp active infra bqs st | i Drain
  Queue ID Pending Drain:          0xffffffff
  Queue ID Pending Drain:          0xffffffff
  Queue ID Pending Drain:          0xffffffff
  Queue ID Pending Drain:          0x9f3b

for Standby SUP:
#show platform hardware qfp standby infra bqs st | i Drain
  Queue ID Pending Drain:          0xffffffff
  Queue ID Pending Drain:          0xffffffff
  Queue ID Pending Drain:          0xffffffff
  Queue ID Pending Drain:          0xffffffff
if any value is not 0xffffffff then the queue with the ID is stuck.

Workaround suggested until a fix is available in future version: Supervisor switchover.

Link to the techzone article: https://techzone.cisco.com/t5/cBR/CPP-Stuck-Queues/ta-p/1102122
Link to CSCvw04657: http://cdets.cisco.com/apps/dumpcr?&content=summary&format=html&identifier=CSCvw04657


Topology:
---------

+------------+        +   +-------------+
|            |        |   |  CBR8-1     |
|            |        +---+             |
|   N S O    +--------+   +-------------+
|            |        |
|            |        |   +-------------+
+------------+        |   |  CBR8-1     |
                      +---+             |
                      |   +-------------+
                      +
                               ...
                      +
                      |
                      |   +-------------+
                      |   |  CBR8-1     |
                      +---+             |
                      +   +-------------+



Preparation of the environment in NSO:
--------------------------------------

It is assumed that you have a running NSO machine. In case you don't have NSO installed you can find detailed information on the installation by accessing the training NSO Essentials for Programmers and Network Architects (NSO201) with your Cisco ID: https://digital-learning.cisco.com/#/course/66475

It is also assumed that the required cisco-ios cli NEDs (Network Element Drivers) are already installed, as well as the CBR8 devices are added to NSO. In case you don't have NEDs and devices ready, below you can find examples for these 2 steps:

1) To install the cisco-ios cli NEDs choose one out of these 3 options (the version used in the example is cisco-ios-cli-3.0 but a newer one can be used as appropriate):

	a)  Extract tar.gz files to the packages directory of your NSO installation directory:
tar -xzvf ~/ncs-5.3/ncs-5.3-cisco-ios-6.40.tar.gz cisco-ios
	
	b)  Copy existing package directories to the packages directory:
cp -r $NCS_DIR/packages/neds/cisco-ios packages/

	c)  Link to existing package directories from the packages directory: 
ln -s $NCS_DIR/packages/neds/cisco-ios packages/cisco-ios

2) Reload packages:
[osboxes@osboxes src]$ ncs_cli -C -u admin
admin connected from 127.0.0.1 using console on osboxes
admin@ncs# packages reload
>>> System upgrade is starting.
>>> Sessions in configure mode must exit to operational mode.
>>> No configuration changes can be performed until upgrade has completed.
>>> System upgrade has completed successfully.
reload-result {
    package cisco-ios-cli-3.0
    result true
}
admin@ncs# show packages package package-version 
                   PACKAGE  
NAME               VERSION  
----------------------------
cisco-ios-cli-3.0  3.0.0.4  


2) To add a device to NSO:

	a) Create an authgroup with the login info from the real device's:
admin@ncs(config)# devices authgroups group myauthgroup default-map remote-name <user> remote-password <password> 
admin@ncs(config-group-myauthgroup)# commit
Commit complete.
admin@ncs(config-group-myauthgroup)# exit

	b) Create device:
admin@ncs(config)# devices device CBR8_MXC address <ip address> authgroup myauthgroup device-type cli ned-id cisco-ios-cli-3.0 
admin@ncs(config-device-CBR8_MXC)# state admin-state unlocked
admin@ncs(config-device-CBR8_MXC)# commit
Commit complete.
admin@ncs(config-device-CBR8_MXC)# ssh fetch-host-keys 
result updated
fingerprint {
    algorithm ssh-rsa
    value 6b:12:77:e2:53:17:9b:2b:ce:89:d1:22:52:7a:38:51
}
admin@ncs(config-device-CBR8_MXC)# end
admin@ncs# 



Steps to use the script:
-----------------------

1) Go to the folder you want to install the script (e.g. /home/user/ncsrun/scripts) in the NSO machine

2) git clone https://github.com/apinelli/nsoCbr8QF.git

3) cd nsoCbr8QF

4) Update nsoCbr8QueueFull.ini file with sender's gmail address/password and recipient's e-mail addresses;

5) Update inventory file with the CBR8 device names present in NSO database that you want to be part of the polling process;

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
