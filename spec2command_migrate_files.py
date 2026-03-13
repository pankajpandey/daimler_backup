# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:51:43 2024

@author: PANKAJ PANDE
"""

import paramiko
from datetime import datetime

def moveFromCCopsviewToSpectrum():
    print ('------ Initiated CCOpsviewToSpectrum file migration -------------------')

    curr_date = datetime.today().strftime('%Y-%m-%d')

    # Local file path to be copied
    local_file_path = "C:/Users/PANKAJP/.spyder-py3/NetCM_Backup/spectrum_devices.xml"
    
    # Remote server details
    server_ip = "53.29.71.110"  # Replace with your server's IP address
    server_port = 22  # Default SSH port is 22
    username = "spectrum"  # Replace with your SSH username
    password = "spectroadmin"  # Replace with your SSH password

    # Path on the remote server
    remote_file_path = "/home/spectrum/spectrum_devices.xml"  # Specify the destination file path

    try:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()
        # Add the server's SSH key automatically
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the server
        ssh.connect(server_ip, port=server_port, username=username, password=password)
        print ('ssh connected...')
        # Use SFTP to upload the file
        sftp = ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)

        print(f"File '{local_file_path}' uploaded to '{remote_file_path}' successfully.")

        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()

    except Exception as e:
         print ('Oops..Failed to copy the file from CCOpsView to Spectrum server',e)
         
         
def readSpectrumDevicesList():
    print ('------ Initiated readSpectrumDevicesList------------------')
    host = "53.29.71.110"
    username = "spectrum"
    password = "spectroadmin"
    curr_date = datetime.today().strftime('%Y-%m-%d')
    command = "stat -c %y /home/spectrum/spectrum_devices.xml"

    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command(command)

        
        # Capture and print the file's modification time
        file_metadata = _stdout.readlines()
        print(f"File modification time: {file_metadata}")
        if file_metadata:
            modification_time = (file_metadata[0]).split(' ')[0]
            print ('modification_time-->',modification_time, ' curr_date-->',curr_date)
            
            if curr_date == modification_time:
                print ('file was copied succssfully', curr_date)
            
        else:
            print("Error fetching file metadata")

        client.close()
    except Exception as e:
         print ('Oops..Failed to read spectrum_to_command_net4all.xml',e)


readSpectrumDevicesList()
#moveFromCCopsviewToSpectrum()