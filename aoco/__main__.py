from aoco.app import App
from aoco.command_manager import CommandManager
from aoco.constants import STORAGE_FILENAME
from aoco.services.advent_of_code import AdventOfCodeService
from aoco.services.argument import ArgumentService
from aoco.services.storage import StorageService

argument_service = ArgumentService()
storage_service = StorageService(STORAGE_FILENAME)
advent_of_code_service = AdventOfCodeService(storage_service)

args = argument_service.parse_args()
cmd = CommandManager(
    advent_of_code_service=advent_of_code_service, storage_service=storage_service
)
app = App(cmd=cmd, args=args)


def main():
    app.run()


if __name__ == "__main__":
    main()
