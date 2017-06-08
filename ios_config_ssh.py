#! /usr/bin/pyhton
#
#  ----------------------------------------------------------------
# Copyright 2017 Cisco Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------
#
# Author:  Fabrizio Maccioni, fabrimac@cisco.com
#
# This software is for demonstration purposes only and is not supported
# by Cisco systems.
#

#
# Script based on netmiko to configure ssh on a Cisco device running IOS XE
#

from netmiko import ConnectHandler
from datetime import datetime

#
# List all the devices
# Make sure the device_type is cisco_ios_telnet (for SSH use cisco_xe)
# FIXME: change USERNAME and PASSWORD
#
USERNAME  = 'cisco'
PASSWORD  = 'cisco'
TRANSPORT = 'cisco_ios_telnet'

cat3k1 = {
'ip': '172.26.249.167',
'username': USERNAME,
'password': PASSWORD,
'device_type': TRANSPORT,
}

cat3k2 = {
'ip': '172.26.249.161',
'username': USERNAME,
'password': PASSWORD,
'device_type': TRANSPORT,
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
