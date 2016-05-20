from fabric.api import run, sudo


def get_home_dir():
    """
    Get home dir of current user
    :return: home dir (string) of current user
    """
    path = run('echo ~')
    return path.strip()


def install_git():
    """
    Install git on host (as Berkshelf depends on it!)

    :return: nothing
    """
    # TODO: add OS switch
    sudo('apt-get update')
    sudo('apt-get install -y git')
