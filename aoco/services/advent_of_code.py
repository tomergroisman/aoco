from aoco.constants import (
    YEAR_KEY,
    SESSION_TOKEN_KEY,
    SESSION_COOKIE_KEY,
)
from aoco.models.solution_result import SolutionResult
from aoco.models.solution_run_state import SolutionRunState
from aoco.services.file import FileService
from aoco.services.network import NetworkService
from aoco.services.solution_runner import (
    SolutionRunnerService,
    create_solution_runner_service,
)
from aoco.services.storage import StorageService
from aoco.utils import (
    get_consumer_day_input_file,
    get_consumer_day_input_test_file,
    get_consumer_day_dir,
    get_consumer_template_file,
    get_consumer_day_solution_file, get_storage_day_key,
)


class AdventOfCodeService:
    def __init__(self, storage_service: StorageService):
        self._storage_service = storage_service
        self._solution_runner_service_by_day: dict[str, SolutionRunnerService] = {}

    def set_input_as_file(self, day: str):
        day_input = self._fetch_day_input(day)
        self._create_day_dir_gracefully(day)
        self._write_day_input_files(day, day_input)
        self._write_day_solution_file_if_missing(day)

    def get_solution_run_state(self, day: str) -> SolutionRunState:
        solution_runner_service = self._get_solution_runner_service(day)
        return solution_runner_service.state

    def run_solution(self, day: str) -> SolutionResult | None:
        solution_runner_service = self._get_solution_runner_service(day)
        if solution_runner_service.state.has_done:
            return None
        answer = solution_runner_service.run()
        return SolutionResult(answer, solution_runner_service.state.is_test)

    def advance_solution(self, day: str, answer: str):
        solution_runner_service = self._get_solution_runner_service(day)
        state = solution_runner_service.state
        should_switch_to_prod_data = state.is_test
        should_submit = not state.is_test
        if should_switch_to_prod_data:
            state.advance_subpart()
        if should_submit:
            self._storage_service.set(get_storage_day_key(day, state.part), answer)
            state.advance_part()

    def _fetch_day_input(self, day: str):
        year = self._storage_service.get(YEAR_KEY)
        session_token = self._storage_service.get(SESSION_TOKEN_KEY)
        return NetworkService.get(
            _get_day_input_url(year, day),
            cookies={SESSION_COOKIE_KEY: session_token},
            as_json=False,
        )

    def _get_solution_runner_service(self, day: str):
        memoized_solution_srunner_service = self._solution_runner_service_by_day.get(
            day
        )
        has_memoized_solution_srunner_service = (
            memoized_solution_srunner_service is not None
        )
        if has_memoized_solution_srunner_service:
            return memoized_solution_srunner_service

        solution_runner_service = create_solution_runner_service(
            day, self._storage_service
        )
        self._solution_runner_service_by_day[day] = solution_runner_service
        return solution_runner_service

    @staticmethod
    def _create_day_dir_gracefully(day: str):
        FileService.create_dir_gracefully(get_consumer_day_dir(day))

    @staticmethod
    def _write_day_input_files(day: str, day_input: str):
        FileService.write(get_consumer_day_input_file(day), day_input)
        FileService.write(get_consumer_day_input_test_file(day), "")

    @staticmethod
    def _write_day_solution_file_if_missing(day: str):
        solution_filename = get_consumer_day_solution_file(day)
        is_missing_solution_file = not FileService.is_file_exists(solution_filename)
        if is_missing_solution_file:
            FileService.copy(get_consumer_template_file(), solution_filename)


def _get_day_input_url(year: str, day: str):
    return f"https://adventofcode.com/{year}/day/{day}/input"

