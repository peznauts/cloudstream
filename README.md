# cloudstream
Tools for setting up a simulcast broadcast using public cloud resources


## Usage

The following create playbook will build an EC2 instance and all associate services to facilitate a streaming connection.

``` shell
$ ansible-playbook -i localhost, ec2-create.yaml -e ansible_python_interpreter=$(which python)
```

