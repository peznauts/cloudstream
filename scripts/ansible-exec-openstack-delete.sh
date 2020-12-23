#!/usr/bin/env bash

~/ansible-venv/bin/ansible-playbook -i localhost, \
                                    -e local_python_interpreter="${HOME}/ansible-venv/bin/python" \
                                    ~/.ansible/collections/ansible_collections/peznauts/cloudstream/playbooks/openstack-delete.yaml
