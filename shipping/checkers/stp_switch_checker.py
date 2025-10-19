import sys
import os

# Get the parent directory path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from time import sleep

from mininet.log import info
from mininet.log import setLogLevel, warn


import subprocess

from threading import Thread


def run_as_sudo(command):
    """
    Runs a command with sudo privileges and exits with the same exit code.
    """
    try:
        # Using subprocess.run to execute the command with sudo
        result = subprocess.run(['sudo'] + command, check=True, text=True)
        # If the command succeeded, exit with a status code of 0
        return 0
    except subprocess.CalledProcessError as e:
        # If the command failed, exit with the command's exit code
        print(f"Command failed with exit code {e.returncode}")
        return e.returncode

def logger(pip):
    line = pip.readline()
    while line:
        info(line)
        line = pip.readline()

def check():
    # # Modify search path for router configuration files.
    # router.DIRECTORY = os.path.join(os.getcwd(), id)

    warn("GRADING\n")
    info("*** Cleaning up using \"sudo mn -c\"\n")
    subprocess.run(["sudo", "mn", "-c"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


    # Task 2
    warn("############################ Starting test cases for Task 3 ############################\n")
    
    info("*** Starting controller\n")
    
    c = subprocess.Popen("ryu-manager stp_switch.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, shell=True)
    #t=Thread(target=logger, args=((c.stderr)))
    #t.start()
    info("*** Wait 5 seconds for controller to start\n")
    sleep(5)  # Wait for all routes to converge.
    
    code = run_as_sudo(["python3", "checkers/check_stp_switch.py"])
    c.terminate()
    sys.exit(code)


if __name__ == "__main__":
    setLogLevel("info")
    check()
