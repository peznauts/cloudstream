# CloudStream

Tools for setting up a simulcast broadcast using public cloud resources. This
project will support simulcasting streams to services like Perascope, Facebook,
Twitch, YouTube, and more.

## Transcoding

CloudStream will detect your configuration and adapt the cloud environment to
meet the needs of your broadcast by splitting off transcoding nodes from the
main relay node. CloudStream allows you to scale your broadcast horizontally
whenever required, which has the added benefit of fencing. By scalling
horizontally, and fencing your broadcast, you'll never need to worry about
one stream negatively impacting another, especially when transcoding is
required.

## Install

This project is an Ansible collection and be easily installed using the
`ansible-galaxy` command line utility.

``` shell
ansible-galaxy collection install git+https://github.com/peznauts/cloudstream.git
```

### Installation

Installation of this collection requires Ansible. Several scripts have been
created in the included "scripts" directory which can assist with the execution
and installation process. Please review the README.md file within the scripts
directory for more information on their uses.

## Setup

This project requires python 3. It is recommended that the execution of these
playbooks comes from package installed Ansible or via a version controlled
virtual environment.

In order to add stream relay endpoints, create a file named `stream-vars.yaml`
in either the provided directory in this repo, **private-vars**, or in a secure
location on your local file system. In this file you can add you private
credentials and stream data.

* The option `rtmpEndpoints` is a list and used to add relay endpoints. Every
  endpoint within this relay scheme will be part of the simulcast.

> The following is an example of what the `stream-vars.yaml` could look like.

``` yaml
---
rtmpEndpoints:
- url: rtmp://endpoint-url.super.streaming.thingame
  key: SuperSecreteKey
- url: rtmp://endpoint-url.super.streaming2.thingame
  key: SuperSecreteKey2
  transcode: 720p30
```

### Extra configuration

Most cloud providers require some additional setup to interact within their
APIs. This section covers the supported cloud providers and where to find the
documentation nessisary to setup the additional configurations.

#### EC2

To interact with the Amazon AWS Cloud you will need to setup some basic
credential files. The basic libray name is called Boto and the documentation
can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration).

> On Windows using the WSL you will need to execute CMD and `bash` to access
  the WSL environment. All credentials will need to be created within the
  home folder of the user. To rapidly get to the home folder simple execute
  `cd ~/` from within the WSL shell.

#### Digital Ocean

Using the Digital Ocean requires you to setup an API OAuth token with both
read and write access. The generated token will need to be saved in the
`~/.ansible/digital-ocean.rc` file location. This file is used by the scripts
to allow for built-in streamdeck integration. The file contents are simple
bash environment variables, which the Digital Ocean modules will use for
authentication.

* Example

``` shell
export DO_API_KEY=XXXyyyZZZ
```

## Usage

This section covers general use cases executing the included playbook from
this collection.

> NOTE: The `local_python_interpreter` extra variable is only required when
running ansible from within a virtual environment.

At the end of the create playbook execution the RTMP URL used in your
broadcasting software will be presented as debug output. This is the URL
used to simulcast your broadcast.

### EC2 Create Usage

The following create playbook will build an EC2 instance and all associate
services to facilitate a streaming connection.

``` shell
$ ansible-playbook -i localhost, \
                   -e local_python_interpreter=$(which python) \
                   -e @private-vars/stream-vars.yaml \  # This is the file which contains the rtmpEndpoints array
                   ~/.ansible/collections/ansible_collections/peznauts/cloudstream/playbooks/ec2-create.yaml
```

### EC2 Delete Usage

The following delete playbook will destroy an EC2 instance and all associate
services for streaming.

``` shell
$ ansible-playbook -i localhost, \
                   -e local_python_interpreter=$(which python) \
                   ~/.ansible/collections/ansible_collections/peznauts/cloudstream/playbooks/ec2-delete.yaml
```

### Digital Ocean Usage

The following create playbook will build an EC2 instance and all associate
services to facilitate a streaming connection.

``` shell
$ source ~/.ansible/digital-ocean.rc  # Source an environment file containing the DigitalOcean oAuth Token.
$ ansible-playbook -i localhost, \
                   -e local_python_interpreter=$(which python) \
                   -e @private-vars/stream-vars.yaml \  # This is the file which contains the rtmpEndpoints array
                   ~/.ansible/collections/ansible_collections/peznauts/cloudstream/playbooks/droplet-create.yaml
```

> NOTE: The above command shows how to include a private variable file which
  contains all of the "secret" options required to configure your server.

### Digital Ocean Delete

``` shell
$ source ~/.ansible/digital-ocean.rc  # Source an environment file containing the DigitalOcean oAuth Token.
$ ansible-playbook -i localhost, \
                   -e local_python_interpreter=$(which python) \
                   ~/.ansible/collections/ansible_collections/peznauts/cloudstream/playbooks/droplet-delete.yaml
```
