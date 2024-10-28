from aoco.constants import INPUT_TEST_FILENAME, INPUT_FILENAME
from aoco.models.solution_run_state import SolutionRunState
from aoco.services.runner import RunnerService
from aoco.services.storage import StorageService
from aoco.utils import get_consumer_day_solution_file, get_storage_day_key


class SolutionRunnerService:
    def __init__(
        self, day: str, state: SolutionRunState, storage_service: StorageService
    ):
        self._day = day
        self._state = state
        self._storage_service = storage_service

    def run(self) -> str:
        args = (
            INPUT_TEST_FILENAME if self._state.is_test else INPUT_FILENAME,
            self._state.part,
        )
        return RunnerService.run_python_script(
            get_consumer_day_solution_file(self._day), *args
        )

    @property
    def state(self) -> SolutionRunState:
        return self._state


def create_solution_runner_service(day: str, storage_service: StorageService):
    has_submitted_part_1 = _get_has_submitted_part_1(day, storage_service)
    has_submitted_part_2 = _get_has_submitted_part_2(day, storage_service)
    has_all_parts_submitted = has_submitted_part_1 and has_submitted_part_2

    state = SolutionRunState(
        is_test=True, part="2" if has_submitted_part_1 else "1", has_done=has_all_parts_submitted
    )
    solution_runner_service = SolutionRunnerService(
        day=day, state=state, storage_service=storage_service
    )

    return solution_runner_service


def _has_submitted_part(day: str, part: str, storage_service: StorageService):
    part_storage_key = get_storage_day_key(day, part)
    return storage_service.get(part_storage_key) is not None


def _get_has_submitted_part_1(day: str, storage_service: StorageService):
    return _has_submitted_part(day=day, part="1", storage_service=storage_service)


def _get_has_submitted_part_2(day: str, storage_service: StorageService):
    return _has_submitted_part(day=day, part="2", storage_service=storage_service)
