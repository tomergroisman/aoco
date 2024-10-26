from pathlib import Path


def get_root_dir():
    return Path(__file__).parent.parent

def get_blueprint_dir():
    return Path.joinpath(get_root_dir(), "blueprint")
