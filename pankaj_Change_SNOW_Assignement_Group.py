import requests

def change_assignment_group():
    print('Inside changing the assignment group')
    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        user = '###########'
        password = '############'

        http_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        https_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        proxies = {
            "http": http_proxy,
            "https": https_proxy
        }

        payload = {'comment': 'Assigning through CCOpsView', 'group': 'GNOC_NET_L1.5_NAFTA'}
        ticket_number = 'INC0223835'  # Replace with the actual ticket number
        assign_group_url = f'https://everest.service-now.com/api/x_infte_sat_mon/monitoring/alert/{ticket_number}'

        response = requests.patch(assign_group_url, json=payload, verify=False, headers=headers, auth=(user, password))
        print('Assignment group has been changed successfully')
    
    except Exception as e:
        print('Failed to change the assignment group', e)

# Example usage:
# change_assignment_group()
