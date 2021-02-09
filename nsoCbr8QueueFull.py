#!/usr/bin/env python

"""Python example script showing proper use of the Cisco Sample Code header.

Copyright (c) {{current_year}} Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

import ncs
import datetime
import smtplib, ssl
import os
import re
import sys
import time
import configparser
from email.mime.text import MIMEText

x = datetime.datetime.now()
path = os.getcwd()
rel_path = (path + "/logs/")

with ncs.maapi.Maapi() as m:
  with ncs.maapi.Session(m, 'admin', 'python'):
    with m.start_write_trans() as t:
        root = ncs.maagic.get_root(t)
        devs = root.devices.device
        installedBase = open('inventory', 'r')

        for line in installedBase:
          show = devs[line].live_status.__getitem__('exec').show
          inp = show.get_input()

    # Check system log
          try:
              inp.args = ['platform hardware qfp active infrastructure bqs status | i Drain']
              r = show.request(inp)
              inp.args = ['platform hardware qfp standby infrastructure bqs status | i Drain']
              r2 = show.request(inp)

    # File write

              filename = x.strftime(line+"_"+"%Y"+"%m"+"%d"+"_"+"%H"+"%M"+".txt")
              abs_file_path = (rel_path + filename)
              message = 'Log: {}'.format(r.result) + '\n'
              message2 = 'Log: {}'.format(r2.result) + '\n'
              print("Polling CBR8s, please wait.......")

              with open(abs_file_path, 'w') as log_file:
                  log_file.write(message)
                  log_file.write(message2)

          except:
              print("Connection failed to " + line)

    # Pause to simulate stuck queue by manually altering the log file

print('Sleeping 30s')
time.sleep(30)

    # Parsing files to look for queue stuck

for file_name in os.listdir(rel_path):
   with open(os.path.join(rel_path, file_name), 'r') as f: # open in readonly mode
      strings = re.findall(r'^Log:.\n^.+0xffffffff\n^.+0xffffffff\n^.+0xffffffff\n^.+0xffffffff\n.+#', f.read(), re.MULTILINE)
      if len(strings) < 2:
          with open(os.path.join(rel_path, file_name), 'r') as g:
            body_text = g.read()

    # Sending the e-mail
    # Reading ini file

            config = configparser.ConfigParser()
            config.read('nsoCbr8QueueFull.ini')

            # read values

            password = config['e-mail']['password']
            sender = config['e-mail']['sender']
            receivers = config['e-mail']['receivers']
            list_receivers = receivers.split(',')

            msg = MIMEText(body_text)

            msg['Subject'] = 'NSO Alert: CBR8 queue stuck detected'
            msg['From'] = sender
            msg['To'] = 'NSO Alert recipients'

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, list_receivers, msg.as_string())
                print('mail successfully sent')
