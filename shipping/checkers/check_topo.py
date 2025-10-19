import sys
import os

# Get the parent directory path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from time import sleep

from topology import PATopo
from topology import IPv4Host

from mininet.link import Link
from mininet.log import error, info
from mininet.log import setLogLevel, warn
from mininet.net import Mininet
from mininet.node import RemoteController

import subprocess


TOPOS = ["star.in", "ring.in"] # all topologies, used in task 1


def find_link(links: list[Link], node1, node2):
    for link in links:
        if link.intf1.node==node1 and link.intf2.node==node2:
            return True
        if link.intf2.node==node1 and link.intf1.node==node2:
            return True
    return False

def check_topology(net: Mininet, lines) -> bool:
    result = True
    hosts = net.hosts
    hosts.sort(key=lambda item: int(item.name[1:]))
    switches = net.switches
    switches.sort(key=lambda item: int(item.name[1:]))
    links = net.links
    
    line = lines[0]
    nums = line.split()
    h = int(nums[0])
    s = int(nums[1])
    l = int(nums[2])
    
    if len(hosts) != h:
        result = False
        warn("Expected "+str(h)+" hosts, found "+str(len(hosts))+"\n")
    if len(switches) != s:
        result = False
        warn("Expected "+str(s)+" switches, found "+str(len(switches))+"\n")
    if len(links) != l:
        result = False
        warn("Expected "+str(l)+" links, found "+str(len(links))+"\n")
    if h*s*l==0:
        warn("Expect at least 1 of link, host, and switch at least, invalid topo\n")
        result = False
    if result:
        lines = lines[1:]
        for i in range(l):
            line = lines[i]
            identifiers = line.split(",")
            src = identifiers[0].strip()
            dest = identifiers[1].strip()
            src_obj = None
            dest_obj = None
            if src[0]=="h":
                src_obj = hosts[int(src[1:])-1]
            elif src[0]=="s":
                src_obj = switches[int(src[1:])-1]
            if dest[0]=="h":
                dest_obj = hosts[int(dest[1:])-1]
            elif dest[0]=="s":
                dest_obj = switches[int(dest[1:])-1]
            if src_obj==None or dest_obj==None:
                raise Exception("Autograder error: Unparsable input: "+line)
            if not find_link(links, src_obj, dest_obj):
                warn("Expect link between "+src_obj.name+" and "+dest_obj.name+", not found\n")
                result = False
    return result
    
def check():

    warn("GRADING\n")
    info("*** Cleaning up using \"sudo mn -c\"\n")
    subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    

    # Task 1
    warn("############################ Starting test cases for Task 1 ############################\n")
    for topo_in in TOPOS:
        subprocess.run(["cp", topo_in, "topology.in"])
        info("*** Creating the network for "+topo_in+" \n")
        net = Mininet(topo=PATopo(), host=IPv4Host, link=Link, controller=RemoteController('c', '127.0.0.1', 6633))

        info("*** Starting the network\n")
        net.start()
        info("*** Waiting for Mininet to start")
        sleep(5)  # Wait for all routes to converge.
        f = open("topology.in", "r")
        lines = f.readlines()
        topology_result = check_topology(net, lines)
        net.stop()
        info("*** Cleaning up\n")
        subprocess.run(["rm", "topology.in"])
        subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        if not topology_result:
            warn("(topology) "+topo_in+" fail\n")
            error("incorrect topology\n")
            exit(201)
        else:
            warn("(topology) "+topo_in+" success\n")
    warn("PASSED: Topology check\n")


if __name__ == "__main__":
    print(os.getcwd())
    setLogLevel("info")
    check()
