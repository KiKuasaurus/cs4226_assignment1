import subprocess
import sys

def run_as_sudo(command):
    """
    Runs a command with sudo privileges and exits with the same exit code.
    """
    try:
        # Using subprocess.run to execute the command with sudo
        result = subprocess.run(['sudo'] + command, check=True, text=True)
        # If the command succeeded, exit with a status code of 0
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        # If the command failed, exit with the command's exit code
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    # Example command to run with sudo
    command_to_run = ['python3', 'checkers/check_topo.py']
    run_as_sudo(command_to_run)
