from typing import Any

from aoco.command_manager import CommandManager
from aoco.constants import INIT_CLI_ARGUMENT


class App:
    def __init__(self, cmd: CommandManager, args: dict[str, Any]):
        self.cmd = cmd
        self.args = args

    def start(self):
        try:
            force_init = self.args.get(INIT_CLI_ARGUMENT, False)
            self.cmd.verify_initialization(force_init=force_init)
            self.cmd.select_day()
        except KeyboardInterrupt:
            exit()
