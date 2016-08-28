# fab-provision

``fab-provision`` is a collection of [fabric](https://github.com/fabric/fabric) tasks to provision a machine with chef-solo.

## Usage

```python
from fabric.api import execute, env
from fab_provision.config import load_config
from fab_provision.provision import provision as do_provisioning


def provision(project, stage):
    load_config(project, stage)
    execute(do_provisioning, hosts=env.hosts)

```

## Configuration

load_config depends on the following folder structure to load the correct configs for given project and stage:

```
* projects
** project_name
*** Berksfile
*** config.yml
*** node.json
*** solo.rb
```

config.yml:

```YAML
stage1:
  hosts:
    - user@stage:22
  user: user
  group: group
  nodejson_mapping:
    KEY: value
  solorrb_mapping:
    KEY: value

stage2:
  hosts:
    - user@stage:22
  user: user
  group: group
  nodejson_mapping:
    KEY: value
  solorrb_mapping:
    KEY: value
```

Use local cookbooks from project specific cookbook-path, Berksfile:

```
cookbook 'my_cookbook', path: '$cookbook_path/my_cookbook'
```

## Contribution and License

Developed by Steven Cardoso <hello@steven266.de> and is licensed under the
terms of a MIT license. Contributions are welcomed and appreciated.
