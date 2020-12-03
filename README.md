# cloudstream
Tools for setting up a simulcast broadcast using public cloud resources

## Setup

This project requires python 3. It is recommended that the execution of these
playbooks comes from package installed Ansible or via a version controlled
virtual environment.

In order to add stream relay endpoints, create a file named `stream-vars.yaml`
in the provided **private-vars** directory. In this file you can add you
private credentials and stream data.

* The option `rtmpEndpoints` is a list and used to add relay endpoints. Every
endpoint within this relay scheme will be part of the simulcast.

> The following is an example of what the `stream-vars.yaml` could look like.

``` yaml
---
rtmpEndpoints:
- url: rtmp://endpoint-url.super.streaming.thingame
  key: SuperSecreteKey
```


## EC2 Create Usage

The following create playbook will build an EC2 instance and all associate
services to facilitate a streaming connection.

> NOTE: The `local_python_interpreter` extra variable is only required when
running ansible from within a virtual environment.

``` shell
$ ansible-playbook -i localhost, -e local_python_interpreter=$(which python) ec2-create.yaml
```

At the end of the playbook execution the RTMP URL used in your broadcasting
software will be presented as debug output. This is the URL used to simulcast
your broadcast.

## EC2 Delete Usage

The following delete playbook will destroy an EC2 instance and all associate
services for streaming.

``` shell
$ ansible-playbook -i localhost, -e local_python_interpreter=$(which python) ec2-delete.yaml
```
