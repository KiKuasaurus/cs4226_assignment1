#!/usr/bin/python

import os, sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info, debug
from mininet.node import Host, RemoteController

def host_to_mac(host_number):
    return "ca:ff:ee:ed:00:" + f'{host_number:0{2}x}'

class IPv4Host(Host):
    def config(self, **params):
        super(IPv4Host, self).config(**params)
        # Disable IPv6
        self.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
        self.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
        self.cmd('sysctl -w net.ipv6.conf.lo.disable_ipv6=1')
        
class PATopo( Topo ):
    "PA topology"

    def build( self ):
        # TODO: Parse the input file topology.in
        with open('topology.in', 'r') as f:
            lines=f.readlines()
        
        nml = lines[0].strip().split()
        num_hosts = int(nml[0])
        num_switches = int(nml[1])
        num_links = int(nml[2])

        # TODO: Add hosts
        # Use the self.addHost(HOST_NAME, mac=MAC_ADDRESS) API
        # For auto-grading purposes
        # The i-th (1-indexed) host will have its host name set to h<i>
        # e.g. the first host should have host name "h1"
        # The MAC_ADDRESS should be retrieved by calling a function host_to_mac(host_name)
        # > host_name = 'h%d' % [HOST_NUMBER]
        # > self.addHost(host_name, mac=host_to_mac([HOST_NUMBER]))
        for i in range(1, num_hosts + 1):
            host_name = 'h%d' % i
            self.addHost(host_name, mac=host_to_mac(i))

        # TODO: Add switches
        # Use the self.addHost(SWITCH_NAME, config) API
        # For auto-grading purposes
        # The i-th (1-indexed) switch will have its host name set to s<i>
        # e.g. the first switch should have host name "s1"
        # > sconfig = {'dpid': "%016x" % [SWITCH NUMBER]}
        # > self.addSwitch('s%d' % [SWITCH NUMBER], **sconfig)
        for i in range(1, num_switches + 1):
            sconfig = {'dpid': "%016x" % i}
            self.addSwitch('s%d' % i, **sconfig)
        
        # TODO: Add links
        # > self.addLink([DEVICE1], [DEVICE2]) 
        for i in range(1, num_links + 1):
            link_info = lines[i].strip().split()
            device1 = link_info[0]
            device2 = link_info[1]
            self.addLink(device1, device2)
        pass
        
                    
def run():
    c = RemoteController('c', '127.0.0.1', 6633)
    net = Mininet(topo=PATopo(), host=IPv4Host, controller=None)
    net.addController(c)
    net.start()

    CLI(net)
    net.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()
