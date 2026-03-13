import requests

def change_state_to_resolve():
    print('Inside changing the state to resolve')
    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        user = '###########'
        password = '#################'

        http_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        https_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        proxies = {
            "http": http_proxy,
            "https": https_proxy
        }

        payload = {'close_note': 'Alarm cleared. Closing by CCOpsView'}
        ticket_number = 'INC###########'  # Replace with the actual ticket number
        resolve_url = f'https://everest.service-now.com/api/x_infte_sat_mon/monitoring/alert/{ticket_number}/resolve'

        response = requests.patch(resolve_url, json=payload, verify=False, headers=headers, auth=(user, password))
        print('Status changed to Resolved')
    
    except Exception as e:
        print('Failed to change the ticket status', e)

# Example usage:
# change_state_to_resolve()
