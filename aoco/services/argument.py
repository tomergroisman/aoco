import argparse

import aoco.strings as s
from aoco.constants import INIT_CLI_ARGUMENT


class ArgumentService:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=s.help_app_name,
            description=s.help_app_description,
        )
        self.parser.add_argument(
            "-i",
            f"--{INIT_CLI_ARGUMENT}",
            action="store_true",
            help=s.help_init_command_description,
        )

    def parse_args(self) -> dict[str, str]:
        return self.parser.parse_args().__dict__
