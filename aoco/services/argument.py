import argparse

from aoco.constants import INIT_CLI_ARGUMENT


class ArgumentService:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Aoco",
            description="Advent of Code helper cli application",
        )
        self.parser.add_argument(
            "-i",
            f"--{INIT_CLI_ARGUMENT}",
            action="store_true",
            help="initialize the configuration for a new AOC project",
        )

    def parse_args(self) -> dict[str, str]:
        return self.parser.parse_args().__dict__
