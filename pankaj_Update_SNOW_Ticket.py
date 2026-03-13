import requests
import logging

log = logging.getLogger(__name__)

def update_snow_ticket(snow_ticket, comment_string, snow_ticket_priority):
    log.info('Inside updating SNOW ticket %s', snow_ticket)
    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        user = '##############'
        password = '#################'

        http_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        https_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        proxies = {
            "http": http_proxy,
            "https": https_proxy
        }

        payload = {'comment': comment_string, 'priority': snow_ticket_priority}
        snow_ticket_url = f'https://everest.service-now.com/api/x_infte_sat_mon/monitoring/alert/{snow_ticket}'

        response = requests.patch(snow_ticket_url, json=payload, verify=False, headers=headers, proxies=proxies, auth=(user, password))
        log.info('Comments updated successfully %s', snow_ticket)

    except Exception as e:
        log.error('Failed to update comments in SNOW ticket %s', e)

# Example usage:
# update_snow_ticket('INC#####', 'Update from CCOpsView.', '2')
