#!/usr/bin/python

"""
Ghozali, Oct 2020
"""

"""
@Student <Wen Yiran/A0105610Y>
Date : 2020 Oct 27
"""


import time


class Automonitor(object):
    def __init__(self, update_interval=1):
        self.update_interval = float(update_interval)
        self.trafficdic = {}

    def get_stats(self, switch, src, dst):
        traffic_info = self.trafficdic.get((switch, src, dst), None)

        if traffic_info is None:
            traffic_info = {}
            traffic_info['bytecount_before'] = 0
            traffic_info['bytecount_current'] = 0
            traffic_info['throughput'] = 0
            self.trafficdic[(switch, src, dst)]=traffic_info
        return traffic_info

    def update_monitor(self, flowget):
        for switch in ["00:00:00:00:00:00:00:01","00:00:00:00:00:00:00:02", "00:00:00:00:00:00:00:03"]:
            retData = flowget.get(switch)
            flows = retData['flows']
            for flow in flows:
                myMatch = flow['match']
                if ('ipv4_src' in myMatch) and ('ipv4_dst' in myMatch):
                    src = myMatch['ipv4_src']
                    dst = myMatch['ipv4_dst']
                    #protocal = 'tcp'
                    # if ('ip_proto' in myMatch) and (myMatch['ip_proto'] == '0x11'):
                    #     protocal = 'udp'
                    traffic_info = self.get_stats(switch, src, dst)
                    traffic_info['bytecount_current'] += int(flow['byteCount'])

        for key, info in self.trafficdic.items():
            info["throughput"] = (info['bytecount_current'] - info['bytecount_before']) * 8 / self.update_interval
            info['bytecount_before'] = info['bytecount_current']
            info['bytecount_current'] = 0
