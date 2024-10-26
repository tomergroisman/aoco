from aoco.constants import YEAR_KEY, SESSION_TOKEN_KEY, SESSION_COOKIE_KEY
from aoco.services.network import NetworkService
from aoco.services.storage import StorageService


class AdventOfCodeService:
    def __init__(self, storage_service: StorageService):
        self._storage_service = storage_service

    def fetch_day_input(self, day: str):
        year = self._storage_service.get(YEAR_KEY)
        session_token = self._storage_service.get(SESSION_TOKEN_KEY)
        return NetworkService.get(
            _get_day_input_url(year, day),
            cookies={SESSION_COOKIE_KEY: session_token},
            as_json=False,
        )

def _get_day_input_url(year: str, day: str):
    return f"https://adventofcode.com/{year}/day/{day}/input"
