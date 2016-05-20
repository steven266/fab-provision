from fabric.api import run, sudo, env, cd, put, settings
from os.path import isdir
from helpers import get_home_dir


def install_chef():
    """
    Installs chef

    :return: nothing
    """

    # check if chef is already installed
    chef_version = '0.12.0-1'
    version = None
    with settings(warn_only=True):
        version = run("dpkg-query --showformat='${Version}' --show chefdk")
    if version == chef_version:
        print "Skip: ChefDK is already installed!"
        return

    # TODO: add OS switch
    # Download package
    run('wget -O %s %s' % (env.chef_installer, env.chef_url))

    # Install package
    sudo('dpkg -i %s' % env.chef_installer)

    # Cleanup
    run('rm -f %s' % env.chef_installer)


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
