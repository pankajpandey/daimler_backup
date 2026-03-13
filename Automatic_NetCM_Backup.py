# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import paramiko
import time

with open('ip_list.txt') as fname:
	ip_list = fname.read().splitlines()
	#print(switches)

with open('creds.txt') as creds:
	cred_rec = creds.read().splitlines()
    

def execute_commands_on_remote(hostname, port, username, password, commands, enable_password):
    print ('current hostname-->',hostname)
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the remote server
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
        with open(hostname+'.txt', 'w') as output_file:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname,port, username, password, look_for_keys=False)
            chan = ssh.invoke_shell()
            time.sleep(1)
            chan.send('config paging disable\n')
            time.sleep(1)

            # for firewalls
            chan.send('show run-config\n')
            time.sleep(20)
              
            output = chan.recv(999999999999)
            print ('output----->',output)
 
            f1 = open('WLC_License/'+hostname+'.txt', 'w')
            f1.write(output.decode("utf-8") )
            f1.close()
            ssh.close() 
            output_file.close()
            print ('Finished--->',hostname)
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the SSH connection
        # ssh_client.close()
        print("Connection closed")

for hostname in ip_list:
    # Define your remote server details and commands
    hostname = hostname
    port = 22  # Default SSH port
    username = cred_rec[0]
    password = cred_rec[1]
    enable_password = cred_rec[1]
    commands = ['show run', 'show clock']
    execute_commands_on_remote(hostname, port, username, password, commands, enable_password)