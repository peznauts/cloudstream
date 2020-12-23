#!/usr/bin/env bash
set -e

source /etc/os-release 2>/dev/null
export DISTRO_ID="${ID}"

case ${DISTRO_ID} in
    centos|rhel)
        dnf -y install python3-virtualenv
        ;;
    ubuntu|debian)
        sudo apt update
        sudo DEBIAN_FRONTEND=noninteractive apt install -y python3-venv
        ;;
    opensuse*)
        zypper -n install -l python-virtualenv
        ;;
esac

set -v

python3 -m venv ~/ansible-venv

~/ansible-venv/bin/pip install wheel pip --force --upgrade
~/ansible-venv/bin/pip install ansible boto boto3 openstacksdk
~/ansible-venv/bin/ansible-galaxy collection install git+https://github.com/peznauts/cloudstream.git
