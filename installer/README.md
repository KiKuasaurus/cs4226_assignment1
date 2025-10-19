# Installing PA1 Environment

These scripts help you install the assignment environment on a fresh Ubuntu 22.04.
We assume an x86-64 architecture.

## Using the Provided VM

If you are using our provided VM, there is one extra step to do.
Please open `~/.bashrc` and comment out the last line. That line is for PA2, we will re-enable it when time comes.
Please open a **NEW** terminal, and continue with the rest of this document.

## Installing Dependencies

Ryu needs Python version <= 3.9 to run. We can achieve this using pyenv.

Copy `dep_setup.sh` into the VM and execute it. You might have to make it executable using `chmod +x <your_copied_script_name>`.

This script will install pyenv, as well as some other dependencies onto the VM.

## Installing Ryu and Mininet 

**AFTER** the script above finishes, open a **NEW** terminal (so that the changes made to `.bashrc` are loaded).

Copy `env_setup.sh` into the VM and execute it. You might have to make it executable using `chmod +x <your_copied_script_name>`.

This script will install python libraries needed. It will also clone both Mininet and Ryu and install those from source.

## Verify your Installation

**AFTER** the scripts above finishes, open another **NEW** terminal (so that the changes made to `.bashrc` are loaded).

Copy `verify_env.sh` into the VM and execute it. You might have to make it executable using `chmod +x <your_copied_script_name>`. If all three commands are found, you are ready to go!

## Common Issues

### -bash: ./*.sh: cannot execute: required file not found

Run `dos2unix *.sh` for the scripts, it will convert the end-of-line characters to unix formats. 

### Help! My gnome-terminal won't even start

Check if your `LANG` setting in `/etc/default/locale` is `en_US.UTF-8`. If not update it using `sudo update-locale LANG=en_US.UTF-8`. (You might need to download `Terminator` from `Ubuntu Software` for this)

### Not in this sudoers file. This incident will be reported

No worries, SPF can't see that report. Hopefully at least you know what is the root password. Change user to root by `su`, and add your account to the `sudo` group by `usermod -aG sudo <your_username>`. Logout and log back in (or reboot, if that is more comfortable). There you should have it.

### Python not found

While not having a huge snake around you might be reassuring, missing python on your VM will definitely be a big issue. This is most likely due to you did not create a new terminal before running `env_setup.sh`, causing the `pyenv` commands to fail. Redo everything after that step in a new terminal.

