from fabric.api import env
from .chef import install_chef, run_berkshelf, put_cookbooks, put_data_bags, run_chef
from .config import put_config
from .helpers import install_git


def provision():
    if env.install_git:
        install_git()
    install_chef()
    put_config()
    put_cookbooks()
    run_berkshelf()
    put_data_bags()
    run_chef()
