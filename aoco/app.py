from typing import Any

from aoco.command_manager import CommandManager
from aoco.constants import INIT_CLI_ARGUMENT


class App:
    def __init__(self, cmd: CommandManager, args: dict[str, Any]):
        self.cmd = cmd
        self.args = args

    def run(self):
        try:
            force_init = self.args.get(INIT_CLI_ARGUMENT, False)
            self.cmd.verify_initialization(force_init=force_init)
            selected_day = self.cmd.select_day()
            self.cmd.watch_solutions(selected_day)
        except KeyboardInterrupt:
            exit()
