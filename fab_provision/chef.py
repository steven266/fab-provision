from fabric.api import run, sudo, env, cd, put, settings
from os.path import isdir
from helpers import get_home_dir


def install_chef():
    """
    Installs chef

    :return: nothing
    """

    if env.chef_dk == 'current':
        run('curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -c current -P chefdk')
    else:
        with settings(warn_only=True):
            version = run("dpkg-query --showformat='${Version}' --show chefdk")
            if version == env.chef_dk:
                print "Skip: ChefDK is already installed!"
                return

        run('curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -v %s -P chefdk' % env.chef_dk)


def run_berkshelf():
    """
    Run Berkshelf (install & vendor)

    :return: nothing
    """
    with cd('~/chef'):
        # Install berksfile and vendor cookbooks
        run('berks install')
        run('berks vendor cookbooks')


def run_chef():
    """
    Run Chef Solo

    :return: nothing
    """
    with cd('~/chef'):
        # Run Chef
        sudo('chef-solo -c ~/chef/solo.rb')


def put_cookbooks():
    """
    Upload project specific cookbooks - if available

    :return: nothing
    """
    path = get_home_dir()
    if isdir('projects/%s/cookbooks' % env.project):
        put('projects/%s/cookbooks' % env.project, '%s/chef' % path)


def put_data_bags():
    """
    Upload project specific data bags - if available

    :return: nothing
    """
    path = get_home_dir()
    if isdir('projects/%s/data_bags' % env.project):
        put('projects/%s/data_bags' % env.project, '%s/chef' % path)
