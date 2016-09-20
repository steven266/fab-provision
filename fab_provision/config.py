from fabric.api import env, sudo, local, run, put
from string import Template
from yaml import load as yaml_load
from json import dumps

from helpers import get_home_dir


def load_config(project, stage):
    """
    Loads configuration for given project and stage

    :param project: The project to load config from
    :param stage: The stage that should be provisioned
    :return: nothing
    """

    env.colorize_errors = True
    env.shell = "/bin/bash -l -i -c"

    if 'chef_dk' not in env:
        env.chef_dk = 'current'

    if 'install_git' not in env:
        env.install_git = False

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
    except TypeError:
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

    for option, value in env.nodejson_mapping.items():
        if type(value) in [dict, list]:
            value = dumps(value)
            env.nodejson_mapping[option] = value


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

    # Generate and upload Berksfile, node.json and solo.rb
    # Create temp folder if necessary
    local('mkdir -p temp')

    """
        Berksfile
    """
    run('mkdir %s/chef/local_cookbooks' % path)

    template = ''
    with open('projects/%s/Berksfile' % env.project, 'r') as config_file:
        template = Template(config_file.read())

    configuration = template.safe_substitute({
        'cookbook_path': '%s/chef/local_cookbooks' % path
    })

    # save configuration in temp folder
    with open('temp/Berksfile_%s_%s' % (env.project, env.stage), 'w') as config_file:
        config_file.write(configuration)

    # put configuration
    put('temp/Berksfile_%s_%s' % (env.project, env.stage), '%s/chef/Berksfile' % path)

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
    local('rm temp/Berksfile_%s_%s' % (env.project, env.stage))
    local('rm temp/solo_%s_%s.rb' % (env.project, env.stage))
    local('rm temp/node_%s_%s.json' % (env.project, env.stage))
