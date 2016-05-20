from fab_provision.chef import install_chef, run_berkshelf, put_cookbooks, run_chef
from fab_provision.config import put_config


def provision():
    install_chef()
    put_config()
    run_berkshelf()
    put_cookbooks()
    run_chef()
