from netmiko import ConnectHandler

import re
import os
import sys
import getpass
import telnetlib
import pandas as pd

# ip='53.242.126.10'
username='pankajp'
password='PanSum4444'

print('========================== Initiated ======================')
from netmiko import ConnectHandler

# Define the list of commands you want to run
# Define the list of commands to execute sequentially
commands = [
    "install remove inactive",  # Clean-up command
    "sh log",                   # Logs verification commands
    "sh log | i flash",
    "sh log | i memory",
    "sh clock",
]

with open('wlc_ip_list.txt') as fname:
    switches = fname.read().splitlines()
    for ip in switches:
        net_conn = {
            'device_type': 'cisco_wlc_ssh',
            'host': ip,
            'username': username,
            'password': password,
            # 'secret': enable_sec,
            'verbose': True,
            'timeout': 30,
            'global_delay_factor': 2,
            'session_log': 'netmiko_session_log.txt'
        }

        try:
            with ConnectHandler(**net_conn) as conn:
                # Check if the device is alive
                if conn.is_alive():
                    try:
                        # Step 1: Execute 'install remove inactive' with confirmation
                        output = conn.send_command_timing("install remove inactive")
                       
                        # Flexible regex to match the confirmation prompt
                        pattern = re.compile(r"Do you want to remove the above files\? \[y/n\]", re.IGNORECASE)
                        
                        if pattern.search(output):
                            print("Pattern detected: Proceeding with confirmation 'y'")
                            output += conn.send_command_timing("y")  # Send confirmation 'y'
                        else:
                            print("Pattern not detected in output")
                        
                        with open(f'WLC_License/{ip}_install_remove_inactive.txt', 'w') as the_file:
                            the_file.write(output)
                        
                        # Step 2: Execute remaining commands
                        for command in commands[1:]:  # Skip the first command as it's already executed
                            output = conn.send_command(command)  
                            print(f"Output for {command} on {ip} --->", len(output))
                            with open(f'WLC_License/{ip}_{command.replace(" ", "_").replace("|", "_")}.txt', 'w') as the_file:
                                the_file.write(output)

                        conn.disconnect()
                    except Exception as e:
                        print('Oops, failed to execute command', e)
                        with open('command_failed_license.txt', 'a') as failed_file:
                            failed_file.write(ip+"\n")
                else:
                    print('Failed to connect to device')
        except Exception as e:
            print('Oops..credentials failed', e)
            with open('credentials_failed_aerospace.txt', 'a') as failed_file:
                failed_file.write(ip+"\n")
print ('------------------finished-----------------------------------')