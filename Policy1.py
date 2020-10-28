#!/usr/bin/python

"""
Ghozali, Oct 2020
"""

"""
@Student Wen Yiran / A0105610Y
Date : 2020 Oct 27
"""

import time
import httplib
import json
from Automonitor import Automonitor

class flowStat(object):
    def __init__(self, server):
        self.server = server

    def get(self, switch):
        ret = self.rest_call({}, 'GET', switch)
        return json.loads(ret[2])

    def rest_call(self, data, action, switch):
        path = '/wm/core/switch/'+switch+"/flow/json"
        headers = {'Content-type': 'application/json','Accept': 'application/json'}
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret


class StaticFlowPusher(object):
    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret


pusher = StaticFlowPusher('127.0.0.1')
flowget = flowStat('127.0.0.1')

monitor = Automonitor(1)
                               
def AutoRouting():
    switched = False
    while True:
        monitor.update_monitor(flowget)
        H1H3connection = monitor.get_stats("00:00:00:00:00:00:00:01", "10.0.0.1", "10.0.0.3")["throughput"]
        #print('tcp throuhgput:  ' , H1H3connection)
        H1H4connection = monitor.get_stats("00:00:00:00:00:00:00:01", "10.0.0.1", "10.0.0.4")["throughput"]
        #print('udp throuhgput:  ' , H1H4connection)
        if H1H3connection+H1H4connection >= 95000000 and not switched:
            switchRoute()
            switched = True

        time.sleep(1)


def switchRoute():
    S1toS2flow = {'switch':"00:00:00:00:00:00:00:01","name":"H1toH2flow","cookie":"0",
                    "priority":"100","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=2"}
    S2toS3flow = {'switch':"00:00:00:00:00:00:00:02","name":"S2toS3flow","cookie":"0",
                    "priority":"100","in_port":"2","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=3"}
    S3toH4flow = {'switch':"00:00:00:00:00:00:00:03","name":"S3toH4flow","cookie":"0",
                    "priority":"100","in_port":"5","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=2"}

    pusher.set(S1toS2flow)
    pusher.set(S2toS3flow)
    pusher.set(S3toH4flow)




"""def udp():
    S1Staticflow1 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh2udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11",
                    "ipv4_src":"10.0.0.1","ipv4_dst":"10.0.0.2","active":"true","actions":"output=2"}
    S1Staticflow2 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h2toh1udp","cookie":"0",
                    "priority":"10","in_port":"2","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S2Staticflow1 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh1udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=2"}
    S2Staticflow2 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h1toh2udp","cookie":"0",
                    "priority":"10","in_port":"2","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}

    S1Staticflow3 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh3udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=3"}
    S1Staticflow4 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h3toh1udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S3Staticflow1 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h3toh1udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=4"}
    S3Staticflow2 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh3udp","cookie":"0",
                    "priority":"10","in_port":"4","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=1"}

    S2Staticflow3 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh3udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=3"}
    S2Staticflow4 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h3toh2udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}
    S3Staticflow3 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h3toh2udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=5"}
    S3Staticflow4 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h2toh3udp","cookie":"0",
                    "priority":"10","in_port":"5","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=1"}

    S1Staticflow5 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh4udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=3"}
    S1Staticflow6 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h4toh1udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S3Staticflow5 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h4toh1udp","cookie":"0",
                    "priority":"10","in_port":"2","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=4"}
    S3Staticflow6 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh4udp","cookie":"0",
                    "priority":"10","in_port":"4","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=2"}

    S2Staticflow5 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh4udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=3"}
    S2Staticflow6 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h4toh2udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}
    S3Staticflow7 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h4toh2udp","cookie":"0",
                    "priority":"10","in_port":"2","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=5"}
    S3Staticflow8 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h2toh4udp","cookie":"0",
                    "priority":"10","in_port":"5","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=2"}

    S1Staticflow7 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh5udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}
    S1Staticflow8 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h5toh1udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S3Staticflow9 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h5toh1udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=4"}
    S3Staticflow10 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh5udp","cookie":"0",
                    "priority":"10","in_port":"4","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}

    S2Staticflow7 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh5udp","cookie":"0",
                    "priority":"10","in_port":"1","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}
    S2Staticflow8 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h5toh2udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}
    S3Staticflow11 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h5toh2udp","cookie":"0",
                    "priority":"10","in_port":"3","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=5"}
    S3Staticflow12 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h2toh5udp","cookie":"0",
                    "priority":"10","in_port":"5","eth_type":"0x800","ip_proto":"0x11","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}

    pusher.set(S1Staticflow1)
    pusher.set(S1Staticflow2)
    pusher.set(S1Staticflow3)
    pusher.set(S1Staticflow4)
    pusher.set(S1Staticflow5)
    pusher.set(S1Staticflow6)
    pusher.set(S1Staticflow7)
    pusher.set(S1Staticflow8)

    pusher.set(S2Staticflow1)
    pusher.set(S2Staticflow2)
    pusher.set(S2Staticflow3)
    pusher.set(S2Staticflow4)
    pusher.set(S2Staticflow5)
    pusher.set(S2Staticflow6)
    pusher.set(S2Staticflow7)
    pusher.set(S2Staticflow8)

    pusher.set(S3Staticflow1)
    pusher.set(S3Staticflow2)
    pusher.set(S3Staticflow3)
    pusher.set(S3Staticflow4)
    pusher.set(S3Staticflow5)
    pusher.set(S3Staticflow6)
    pusher.set(S3Staticflow7)
    pusher.set(S3Staticflow8)
    pusher.set(S3Staticflow9)
    pusher.set(S3Staticflow10)
    pusher.set(S3Staticflow11)
    pusher.set(S3Staticflow12)
"""


def staticForwarding():
    S1Staticflow1 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh2","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=2"}
    S1Staticflow2 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h2toh1","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S2Staticflow1 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh1","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=2"}
    S2Staticflow2 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h1toh2","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}

    S1Staticflow3 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh3","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=3"}
    S1Staticflow4 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h3toh1","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S3Staticflow1 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h3toh1","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=4"}
    S3Staticflow2 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh3","cookie":"0",
                    "priority":"1","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=1"}

    S2Staticflow3 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh3","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=3"}
    S2Staticflow4 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h3toh2","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}
    S3Staticflow3 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h3toh2","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=5"}
    S3Staticflow4 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h2toh3","cookie":"0",
                    "priority":"1","in_port":"5","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=1"}

    S1Staticflow5 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh4","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=3"}
    S1Staticflow6 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h4toh1","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S3Staticflow5 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h4toh1","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=4"}
    S3Staticflow6 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh4","cookie":"0",
                    "priority":"1","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=2"}

    S2Staticflow5 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh4","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=3"}
    S2Staticflow6 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h4toh2","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}
    S3Staticflow7 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h4toh2","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=5"}
    S3Staticflow8 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h2toh4","cookie":"0",
                    "priority":"1","in_port":"5","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=2"}

    S1Staticflow7 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh5","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}
    S1Staticflow8 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h5toh1","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=1"}
    S3Staticflow9 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h5toh1","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=4"}
    S3Staticflow10 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh5","cookie":"0",
                    "priority":"1","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}

    S2Staticflow7 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh5","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}
    S2Staticflow8 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h5toh2","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}
    S3Staticflow11 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h5toh2","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=5"}
    S3Staticflow12 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h2toh5","cookie":"0",
                    "priority":"1","in_port":"5","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=3"}

    pusher.set(S1Staticflow1)
    pusher.set(S1Staticflow2)
    pusher.set(S1Staticflow3)
    pusher.set(S1Staticflow4)
    pusher.set(S1Staticflow5)
    pusher.set(S1Staticflow6)
    pusher.set(S1Staticflow7)
    pusher.set(S1Staticflow8)

    pusher.set(S2Staticflow1)
    pusher.set(S2Staticflow2)
    pusher.set(S2Staticflow3)
    pusher.set(S2Staticflow4)
    pusher.set(S2Staticflow5)
    pusher.set(S2Staticflow6)
    pusher.set(S2Staticflow7)
    pusher.set(S2Staticflow8)

    pusher.set(S3Staticflow1)
    pusher.set(S3Staticflow2)
    pusher.set(S3Staticflow3)
    pusher.set(S3Staticflow4)
    pusher.set(S3Staticflow5)
    pusher.set(S3Staticflow6)
    pusher.set(S3Staticflow7)
    pusher.set(S3Staticflow8)
    pusher.set(S3Staticflow9)
    pusher.set(S3Staticflow10)
    pusher.set(S3Staticflow11)
    pusher.set(S3Staticflow12)


if __name__ =='__main__':
    staticForwarding()
    #udp()
    AutoRouting()
    pass
