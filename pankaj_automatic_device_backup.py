import netmiko
from netmiko import ConnectHandler
import getpass

def ssh_login(device, username, password):
    try:
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': device,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**ios_device)
        print(device, " : SSH login Successful")
        return net_connect
    except netmiko.ssh_exception.NetMikoTimeoutException:
        print(f'{device}: SSH connection timed out')
        return None
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print(f'{device}: Authentication failed')
        return None
    except Exception as e:
        print(f'{device}: An error occurred - {str(e)}')
        return None

def fetch_and_save_config(net_connect, device, success_list, failed_list):
    if net_connect:
        try:
            output = net_connect.send_command("show run\n")
            if output:
                lines = output.splitlines()
                if len(lines) > 10:
                    formatted_output = '\n'.join(lines)
                    filename = f"{device}.txt"
                    with open(filename, "a+") as file:
                        file.write(f"-----------------------{device}----------conf start---------------------\n")
                        file.write(f"{formatted_output}\n")
                        file.write(f"=============================={device}=========conf end=================\n")
                        print(f'Backup for {device} done successfully')
                        success_list.append(device)
            else:
                print(f'Configuration not fetched for {device}.')
                failed_list.append(device)
        except Exception as e:
            print(f'Error while fetching configuration for {device} - {str(e)}')
            failed_list.append(device)

def main():
    # Read device IPs from the file
    with open('ip_list10.txt') as fname:
        switches = fname.read().splitlines()

    # Input credentials securely
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    success = []
    failed = []

    with open('DeviceUPDetails.txt', 'w+') as file:
        print("Trying SSH Test for User ID:", username, "Password: ******** ")
        for device in switches:
            net_connect = ssh_login(device, username, password)
            if net_connect:
                fetch_and_save_config(net_connect, device, success, failed)
                net_connect.disconnect()

    print('Successful backup:', success)
    print('Failed backup:', failed)

if __name__ == "__main__":
    main()
