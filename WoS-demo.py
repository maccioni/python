import smtplib
import requests
import json
import re
import os
import subprocess


### Disable invalid certificate warnings.
requests.packages.urllib3.disable_warnings()

def createserviceticket():
    response = requests.post(
        url="https://172.26.249.155/api/v1/ticket",
        headers={
            "Content-Type": "application/json",
        },
        verify=False,
        data=json.dumps({
            "username": 'admin',
            "password": 'C!sco123'
        })
    )
    output = ('Response HTTP Response Body: {content}'.format(content=response.content))
    match_service_ticket = re.search('serviceTicket":"(.*cas)', output, flags=0)
    service_ticket = match_service_ticket.group(1)
    return service_ticket

url = "https://172.26.249.155/api/v1/network-device"

response = requests.get(url,headers={"X-Auth-Token": createserviceticket(),"Content-Type": "application/json",},verify=False)

data = response.json()

#print data

print 'Device list:'
device_list = data['response']
for device in device_list:
#    print device['managementIpAddress']
    IP = device['managementIpAddress']
    print IP
#    os.system("echo testo 'TEXT'")
#    os.system("echo ", device['managementIpAddress'])
#    subprocess.call(["echo", IP], shell=True)
#    subprocess.call(["echo", device['managementIpAddress']], shell=True)
