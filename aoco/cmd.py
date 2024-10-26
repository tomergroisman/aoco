from aoco.constants import SESSION_TOKEN_KEY, YEAR_KEY, SESSION_COOKIE_KEY
from aoco.services.network import NetworkService
from aoco.services.prompt import PromptService
from aoco.services.storage import StorageService


class Cmd:
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service

    def verify_initialization(self):
        session_token = self.storage_service.get(SESSION_TOKEN_KEY)
        year = self.storage_service.get(YEAR_KEY)
        has_session_token_not_set = session_token is None
        has_year_not_set = year is None
        should_initialize = has_session_token_not_set or has_year_not_set
        if should_initialize:
            self._set_session_token()
            self._set_year()

    def select_day(self):
        year = self.storage_service.get(YEAR_KEY)
        session_token = self.storage_service.get(SESSION_TOKEN_KEY)
        selected_day = PromptService.list(
            "Select day", [(day, f"Day {day}") for day in range(1, 26)]
        )
        input = NetworkService.get(
            _get_day_input_url(year, selected_day),
            cookies={SESSION_COOKIE_KEY: session_token},
            as_json=False,
        )
        print(input)

    def _set_year(self):
        year = PromptService.text("For what year are you challenging?")
        self.storage_service.set(YEAR_KEY, year)

    def _set_session_token(self):
        session_token = PromptService.text(
            "Please provide your Advent of Code session token?"
        )
        self.storage_service.set(SESSION_TOKEN_KEY, session_token)


def _get_day_input_url(year: str, day: str):
    return f"https://adventofcode.com/{year}/day/{day}/input"
