import sys
import os

# Get the parent directory path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from argparse import ArgumentParser
from dataclasses import dataclass
from time import sleep

from topology import PATopo
from topology import IPv4Host

from mininet.link import Link
from mininet.log import error, info
from mininet.log import output as out
from mininet.log import setLogLevel, warn
from mininet.net import Mininet
from mininet.node import RemoteController


import subprocess
CG_TOPO = "ring.in" # cyclic topology, used in task 3

def run_command_and_capture_output(command):
    # Run the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Read all the output lines from stdout
    output_lines = process.stdout.readlines()

    # Wait for the process to complete
    process.wait()

    return output_lines

def check():
    # # Modify search path for router configuration files.
    # router.DIRECTORY = os.path.join(os.getcwd(), id)
    
    subprocess.run(["cp", CG_TOPO, "topology.in"])
    info("*** Creating the network for "+CG_TOPO+" \n")
    cont = RemoteController('c', '127.0.0.1', 6633)
    net = Mininet(topo=PATopo(), host=IPv4Host, link=Link, controller=None)
    net.addController(cont)
    
    info("*** Starting the network\n")
    net.start()
    info("*** Wait 120 seconds for STP to converge\n")
    for i in range(12):
        sleep(10)  # Wait for all routes to converge.
        info(str(120-(i+1)*10)+"s ")
    info("\n")
    
    
    
    ploss = net.pingAll(1)
    if ploss!=0:
        warn("(stp switch) pingAll failed, "+str(ploss)+"% packets lost\n")
        error("connectivity error")
        net.stop()
        info("*** Cleaning up\n")
        subprocess.run(["rm", "topology.in"])
        subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        exit(204)
    info("*** Wait 5 seconds all flow rules to be properly installed\n")
    sleep(5)
    switches = net.switches
    hosts = net.hosts
    for switch in switches:
        sname = switch.name
        flows = run_command_and_capture_output(["sudo","ovs-ofctl","dump-flows",sname])
        for host in hosts:
            target = "dl_dst="+str(host.MAC())
            found = False
            for flow in flows:
                if target in flow:
                    #info("Flow entry found: "+flow+" for target "+target+" on switch "+sname+"\n")
                    found = True
                    break
            if not found:
                warn("(stp switch) did not find any flow with "+host.name+" as destination on switch "+switch.name+"\n")
                print(flows)
                error("flow error\n")
                net.stop()
                info("*** Cleaning up\n")
                subprocess.run(["rm", "topology.in"])
                subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                exit(205)
            target = "dl_src="+str(host.MAC())
            found = False
            for flow in flows:
                if target in flow:
                    #info("Flow entry found: "+flow+" for target "+target+" on switch "+sname+"\n")
                    found = True
                    break
            if not found:
                warn("(stp switch) did not find any flow with "+host.name+" as source on switch "+switch.name+"\n")
                print(flows)
                error("flow error\n")
                net.stop()
                info("*** Cleaning up\n")
                subprocess.run(["rm", "topology.in"])
                subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                exit(205)
    warn("PASSED: STP switch check\n")
    net.stop()
    info("*** Cleaning up\n")
    subprocess.run(["rm", "topology.in"])
    subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)



if __name__ == "__main__":
    setLogLevel("info")
    check()