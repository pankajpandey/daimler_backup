import datetime
import requests
from flask import Flask, jsonify

def fetch_gnoc_records():
    try:
        print('fetch_gnoc_records ----> initiated <--------------')
        
        now = datetime.datetime.now()
        today = now.strftime('%Y-%m-%d %H:%M:%S')
        print('inside detect on hold tickets', today)

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        user = '#################'
        password = '#################'

        http_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        https_proxy = "security-proxy.emea.svc.corpintra.net:3128"
        proxies = {
            "http": http_proxy,
            "https": https_proxy
        }

        state_list = {'1': 'New', '2': 'In_Progress', '3': 'On_Hold', '4': 'In_Queue', '5': 'Assigned', '6': 'Resolved', '7': 'Closed', '8': 'Cancelled'}
        assignment_list = {'b8049c429777c994709cb5e3f153afe6': 'GNOC_NW_L1.5_Support'}

        assignment_groups = list(assignment_list.keys())
        page_length = 50
        sn_tickets = []

        for group in assignment_groups:
            offset = 0
            try:
                print('current group ------>', group)
                while True:
                    service_now_url = "https://everest.service-now.com/api/x_infte_everest_st/data_pull_api/data/incident?query=assignment_group="+group+"^state=3&page_length=" + str(page_length) + "&offset=" + str(offset)
                    alarm_details_obj = requests.get(service_now_url, verify=False, headers=headers, proxies=proxies, auth=(user, password))
                    sn_tickets_obj = alarm_details_obj.json()['result']['data']

                    if len(sn_tickets_obj) > 0:
                        offset = offset + page_length
                        print(' total service now tickets --->', len(sn_tickets_obj))
                        
                        for t in sn_tickets_obj:
                            service_offering = t['cmdb_ci']['display_value']
                            short_description = t['short_description']['value']
                            sn_tickets.append({
                                'ticketNumber': t['number']['value'],
                                'priority': t['priority']['value'],
                                'shortDescription': short_description,
                                'state': state_list[str(t['state']['value'])],
                                'assignmentGroup': assignment_list[t['assignment_group']['value']],
                                'serviceOffering': service_offering
                            })
                    else:
                        print('no records left for', group)
                        break
            except Exception as e:
                print('Oops. Failed to fetch daily SN tickets', e)
        
        print('sn_tickets prod -->', len(sn_tickets))
        return jsonify({'gnoc_records': sn_tickets}), 200

    except Exception as e:
        print('Oops.. Failed to extract on-hold SNOW tickets', e)
