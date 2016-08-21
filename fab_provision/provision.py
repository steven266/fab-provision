from .chef import install_chef, run_berkshelf, put_cookbooks, put_data_bags, run_chef
from .config import put_config


def provision():
    install_chef()
    put_config()
    run_berkshelf()
    put_cookbooks()
    put_data_bags()
    run_chef()
