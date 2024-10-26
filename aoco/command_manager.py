import aoco.strings as s
from aoco.constants import SESSION_TOKEN_KEY, YEAR_KEY, BLUEPRINT_TARGET_DIRNAME
from aoco.services.advent_of_code import AdventOfCodeService
from aoco.services.file import FileService
from aoco.services.prompt import PromptService
from aoco.services.storage import StorageService
from aoco.utils import get_blueprint_dir


class CommandManager:
    def __init__(
        self,
        advent_of_code_service: AdventOfCodeService,
        storage_service: StorageService,
    ):
        self.advent_of_code_service = advent_of_code_service
        self.storage_service = storage_service

    def verify_initialization(self, force_init: bool):
        should_initialize = force_init or self._has_prerequisites_violation
        if should_initialize:
            self._initialize()

    def select_day(self):
        selected_day = PromptService.select(
            s.day_selection_select_day,
            [(day, f"{s.day_selection_day} {day}") for day in range(1, 26)],
        )
        input = self.advent_of_code_service.fetch_day_input(selected_day)
        print(input)

    def _initialize(self):
        print(">>> in init")
        # self._set_storage()
        self._set_blueprint()

    def _set_year(self):
        year = PromptService.text(s.init_selection_year)
        self.storage_service.set(YEAR_KEY, year)

    def _set_session_token(self):
        session_token = PromptService.text(s.init_selection_session)
        self.storage_service.set(SESSION_TOKEN_KEY, session_token)

    def _set_storage(self):
        self._set_session_token()
        self._set_year()

    @staticmethod
    def _set_blueprint():
        blueprint_dir = get_blueprint_dir()
        FileService.copy_tree(blueprint_dir, BLUEPRINT_TARGET_DIRNAME)

    @property
    def _has_prerequisites_violation(self):
        session_token = self.storage_service.get(SESSION_TOKEN_KEY)
        year = self.storage_service.get(YEAR_KEY)
        has_session_token_not_set = session_token is None
        has_year_not_set = year is None
        return has_session_token_not_set or has_year_not_set


def _get_day_input_url(year: str, day: str):
    return f"https://adventofcode.com/{year}/day/{day}/input"
