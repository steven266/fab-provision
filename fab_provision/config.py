from fabric.api import env, sudo, local, run, put
from string import Template
from yaml import load as yaml_load

from helpers import get_home_dir


def load_config(project, stage):
    """
    Loads configuration for given project and stage

    :param project: The project to load config from
    :param stage: The stage that should be provisioned
    :return: nothing
    """

    # TODO: load chef version set in config
    env.colorize_errors = True
    env.shell = "/bin/bash -l -i -c"
    env.chef_installer = "chefdk_0.12.0-1_amd64.deb"
    env.chef_url = 'https://packages.chef.io/stable/ubuntu/12.04/chefdk_0.12.0-1_amd64.deb'

    env.project = project
    env.stage = stage

    try:
        with open('projects/%s/config.yml' % project, 'r') as ymlfile:
            config = yaml_load(ymlfile)
    except IOError:
        raise Exception('Project or config not defined!')

    try:
        _temp = config[stage]
    except KeyError:
        raise Exception('Stage not defined!')

    for option, value in _temp.items():
        setattr(env, option, value)

    try:
        env.nodejson_mapping['PROJECT'] = project
        env.nodejson_mapping['STAGE'] = stage
    except AttributeError:
        env.nodejson_mapping = {
            'PROJECT': project,
            'STAGE': stage
        }

    try:
        env.solorb_mapping['PROJECT'] = project
        env.solorb_mapping['STAGE'] = stage
    except AttributeError:
        env.solorb_mapping = {
            'PROJECT': project,
            'STAGE': stage
        }


def put_config():
    """
    Upload config files

    :return: nothing
    """
    # Cleanup old chef path
    sudo('rm -rf ~/chef')

    # Create chef path
    run('mkdir ~/chef')

    # Set Home Directory
    path = get_home_dir()
    env.nodejson_mapping['HOME_DIR'] = path
    env.solorb_mapping['HOME_DIR'] = path

    # Upload Berksfile
    put('projects/%s/Berksfile' % env.project, '%s/chef/Berksfile' % path)

    # Generate and upload node.json and solo.rb
    # Create temp folder if necessary
    local('mkdir -p temp')

    """
        node.json
    """
    template = ''
    with open('projects/%s/node.json' % env.project, 'r') as config_file:
        template = Template(config_file.read())

    configuration = template.safe_substitute(env.nodejson_mapping)

    # save configuration in temp folder
    with open('temp/node_%s_%s.json' % (env.project, env.stage), 'w') as config_file:
        config_file.write(configuration)

    # put configuration
    put('temp/node_%s_%s.json' % (env.project, env.stage), '%s/chef/node.json' % path)

    """
        solo.rb
    """
    template = ''
    with open('projects/%s/solo.rb' % env.project, 'r') as config_file:
        template = Template(config_file.read())

    configuration = template.safe_substitute(env.solorb_mapping)

    # save configuration in temp folder
    with open('temp/solo_%s_%s.rb' % (env.project, env.stage), 'w') as config_file:
        config_file.write(configuration)

    # put configuration
    put('temp/solo_%s_%s.rb' % (env.project, env.stage), '%s/chef/solo.rb' % path)

    # cleanup local files
    local('rm temp/solo_%s_%s.rb' % (env.project, env.stage))
    local('rm temp/node_%s_%s.json' % (env.project, env.stage))
