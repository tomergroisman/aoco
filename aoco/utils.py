from pathlib import Path

from aoco.constants import CONSUMER_ROOT_DIRNAME, INPUT_FILENAME, INPUT_TEST_FILENAME, TEMPLATE_FILENAME, \
    SOLUTION_FILENAME


def get_root_dir():
    return Path(__file__).parent.parent

def get_blueprint_dir():
    return Path.joinpath(get_root_dir(), "blueprint")

def get_consumer_template_file():
    return Path.joinpath(Path(CONSUMER_ROOT_DIRNAME), TEMPLATE_FILENAME)

def get_consumer_day_dir(day: str):
    return Path.joinpath(Path(CONSUMER_ROOT_DIRNAME), f"days/day{day}")

def get_consumer_day_solution_file(day: str):
    return Path.joinpath(get_consumer_day_dir(day), SOLUTION_FILENAME)

def get_consumer_day_input_file(day: str):
    return Path.joinpath(get_consumer_day_dir(day), INPUT_FILENAME)

def get_consumer_day_input_test_file(day: str):
    return Path.joinpath(get_consumer_day_dir(day), INPUT_TEST_FILENAME)

def get_storage_day_key(day: str, part: str):
    return f"day_{day}|part_{part}"
