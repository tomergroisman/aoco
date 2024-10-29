import re
from time import sleep
from termcolor import colored
from termcolor._types import Color

import aoco.strings as s
from aoco.constants import SESSION_TOKEN_KEY, YEAR_KEY, CONSUMER_ROOT_DIRNAME
from aoco.services.advent_of_code import AdventOfCodeService
from aoco.services.file import FileService
from aoco.services.logger import LoggerService
from aoco.services.prompt import PromptService
from aoco.services.storage import StorageService
from aoco.utils import (
    get_blueprint_dir,
    get_consumer_days_dir,
    clear,
    get_consumer_day_dir,
)


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

    def select_day(self) -> str:
        initial_date = self._get_last_finished_day() + 1
        selected_day = PromptService.select(
            text=s.day_selection_select_day,
            options=[(day, s.day_selection_day(str(day))) for day in range(1, 26)],
            initial_value=initial_date,
        )
        if not FileService.is_dir_exists(get_consumer_day_dir(selected_day)):
            self.advent_of_code_service.set_input_as_file(selected_day)
        return selected_day

    def watch_solutions(self, day: str):
        while True:
            clear()
            self._print_solution_run_header(day)
            result = self.advent_of_code_service.run_solution(day)
            has_already_submitted = result is None
            if has_already_submitted:
                return LoggerService.log(s.run_phase_well_done)

            continue_message = (
                s.run_phase_should_continue
                if result.is_test
                else s.run_phase_should_submit
            )
            self._print_answer(result.answer)
            should_continue = PromptService.confirm(continue_message)
            sleep(0.5)
            if should_continue:
                self.advent_of_code_service.advance_solution(day, answer=result.answer)

    def _initialize(self):
        self._set_storage()
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

    def _print_solution_run_header(self, day: str):
        color: Color = "blue"
        solution_run_state = self.advent_of_code_service.get_solution_run_state(day)
        text = colored(s.run_phase_header_prefix, color=color, attrs=["bold", "reverse"])
        text += colored(f"\t{s.run_phase_header(solution_run_state.part, day)}", color=color, attrs=["bold"])
        if solution_run_state.is_test:
            text += colored(f" {s.run_phase_header_suffix}", color=color)
        LoggerService.log(text)

    @staticmethod
    def _print_answer(answer: str):
        LoggerService.log(f"\t{s.run_phase_answer(colored(answer, attrs=["bold"]))}\n")


    @staticmethod
    def _set_blueprint():
        blueprint_dir = get_blueprint_dir()
        consumer_days_dir = get_consumer_days_dir()
        FileService.copy_tree(blueprint_dir, CONSUMER_ROOT_DIRNAME)
        FileService.mkdir(consumer_days_dir)

    @staticmethod
    def _get_last_finished_day() -> int:
        finished_days_dir_names = sorted(FileService.dir_content(get_consumer_days_dir()))
        finished_days = [
            int(re.search(r"\d+", day_dir_name).group())
            for day_dir_name in finished_days_dir_names
        ]
        return finished_days[-1] if finished_days else 0

    @property
    def _has_prerequisites_violation(self):
        session_token = self.storage_service.get(SESSION_TOKEN_KEY)
        year = self.storage_service.get(YEAR_KEY)
        has_session_token_not_set = session_token is None
        has_year_not_set = year is None
        return has_session_token_not_set or has_year_not_set
