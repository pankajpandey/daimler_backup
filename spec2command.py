# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:51:43 2024

@author: PANKAJP
"""

import paramiko
from datetime import datetime

def detectSpectrumCommandSync():
    print ('------ Initiated spec2command detection-------------------')
    host = "53.29.71.110"
    username = "spectrum"
    password = "spectroadmin"
    curr_date = datetime.today().strftime('%Y%m%d')

    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command("cat /home/spectrum/command-interface/log/log.txt")

        net_dump = _stdout.readlines()        
        #print('net_dump--->',net_dump)
        today_recs = []
        for rec in net_dump:
            if rec.startswith(curr_date):
                today_recs.append(rec)
        print ('today_recs--->',today_recs)
        if len(today_recs) > 0:
            rec_detection = [d for d in today_recs if 'talend job exited with return code 0' in d]
            if len(rec_detection) > 0:
                print ('Spectrum-command sync is working as intended', curr_date)
            else:
                print ('Spectrum-command sync has failed',curr_date)
        else:
            print ('Spectrum-command sync has failed',curr_date)
        client.close()
    except Exception as e:
         print ('Oops..Failed to check the spectrum-command sync',e)
         
detectSpectrumCommandSync()