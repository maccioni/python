#! /usr/bin/pyhton

from netmiko import ConnectHandler
from datetime import datetime

#
# List all the devices
# Make sure the device_type is cisco_ios_telnet (for SSH use cisco_xe)
#
cat3k1 = {
'device_type': 'cisco_ios_telnet',
'ip': '172.26.249.167',
'username': 'cisco',
'password': 'cisco',
}

cat3k2 = {
'device_type': 'cisco_ios_telnet',
'ip': '172.26.249.161',
'username': 'cisco',
'password': 'cisco',
}
all_devices = [cat3k1, cat3k2]

#
# List all the commands
# Make sure the hostname is already set otherwise add a command at the top of list to set it up
# "ip ssh version 2" is optional as well as the timeouts:
# "ip ssh [time-out seconds | authentication-retries integer]"
#
config_commands = ['ip domain name cisco.com', 'crypto key generate rsa modulus 1024', ' ip ssh version 2']

start_time = datetime.now()

#
# configure the device one by one.
#
# the DELAY_FACTOR is used in send_config_commands() and it is needed beacuse it take
# some some time to generate the rsa keys
# Tune up this value if you want to speed the script up
#
DELAY_FACTOR = 15
for a_device in all_devices:
    print "Configuring " + a_device['ip']
    try:
        net_connect = ConnectHandler(**a_device)
        net_connect.find_prompt()
        output = net_connect.send_config_set(config_commands, delay_factor=DELAY_FACTOR)
        print output
        print  a_device['ip'] + " configured!"
    except Exception as e:
        print "Error configuring %s: %s" %  (a_device['ip'], str(e))
        pass

end_time = datetime.now()
total_time = end_time - start_time 
print "total execution time (h:m:s): " + str(total_time)
