# CloudStream Scripts

The following scripts can be used to help automate deployment scenarios or
provide inspiration on how you can self-automate different scenarios.

## Windows

To run this collection on a Windows the
[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) is
required. Assuming the WSL is in place, the `cmd` scripts will execute basic
software install and execute playbooks accordingly. 

> Some cloud provider executions may be require additional setup.

Installation on windows is simple. The `windows-wsl-venv-install.cmd`
script can be used to install all of the system depencies required to execute
the various cloud provider playbooks. This will require you to enter the
WSL user password.

> To use any of the **cmd** scripts you can execute them from the Windows
  terminal. You can also double click the **cmd** scripts to execute them
  from your desktop.

## Linux

Within a linux environment, the `venv-install.sh` script can be used to install
all system dependencies. The python dependencies will be install in a virtual
environment within the users home folder under `~/ansible-venv`. This script
will require escalated privledges to ensure base packages are installed. 
