##In production, we have front end to accept the config commands, username & password to process the request.
import netmiko
from netmiko import ConnectHandler
import getpass

# Read device IPs from the file
with open('ip_list.txt') as fname:
    switches = fname.read().splitlines()

# Input credentials securely
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

# Open log file
with open('configuration_logs.txt', 'w+') as file:
    for device in switches:
        try:
            ios_device = {
                'device_type': 'cisco_ios',
                'ip': device,
                'username': username,
                'password': password,
            }

            config_commands = [
                'no username dailanfs',
                'no enable secret',
                'username dailanfs password ####',
                'enable secret 5 ####',
                'end',
                'write mem'
            ]

            # Attempt to connect
            net_connect = ConnectHandler(**ios_device)
            print(device, " : SSH login Successful")
            file.write(str(device) + " : SSH login Successful" + "\n")

            output = net_connect.send_config_set(config_commands)
            print(output)
            print("Configuration done Successfully.")
            file.write(device + ': config done successfully' + "\n")
            file.write(output)
            file.write("\n" + "==" * 45 + "\n")
        except netmiko.ssh_exception.NetMikoTimeoutException:
            print(f'{device}: SSH connection timed out')
            file.write(f'{device}: SSH connection timed out\n')
        except netmiko.ssh_exception.NetMikoAuthenticationException:
            print(f'{device}: Authentication failed')
            file.write(f'{device}: Authentication failed\n')
        except Exception as e:
            print(f'{device}: An error occurred - {str(e)}')
            file.write(f'{device}: An error occurred - {str(e)}\n')
