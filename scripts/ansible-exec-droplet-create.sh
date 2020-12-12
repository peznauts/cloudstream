#!/usr/bin/env bash
. ~/.ansible/digital-ocean.rc
~/ansible-venv/bin/ansible-playbook -i localhost, \
                                    -e local_python_interpreter="${HOME}/ansible-venv/bin/python" \
                                    -e @~/.ansible/stream-vars.yaml \
                                    ~/.ansible/collections/ansible_collections/peznauts/cloudstream/playbooks/droplet-create.yaml
