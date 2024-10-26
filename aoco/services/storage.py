from typing import Callable

from aoco.constants import KEY_VALUE_DELIMITER
from aoco.services.file import FileService


class StorageService:
    def __init__(self, storage_filename: str) -> None:
        FileService.create_gracefully(storage_filename)
        self._storage_filename = storage_filename
        self._storage = self._create_storage_from_storage_file()

    def get(self, key: str) -> str | None:
        return self._storage.get(key)

    def set(self, key: str, value: str) -> None:
        self._storage.update({key: value})
        self._update_storage_file()

    def _create_storage_from_storage_file(self) -> dict[str, str]:
        storage_str = FileService.read(self._storage_filename)
        storage_rows = storage_str.split("\n")[:-1]
        return {
            key: value
            for [key, value] in map(_split_by(KEY_VALUE_DELIMITER), storage_rows)
        }

    def _update_storage_file(self) -> None:
        updated_storage_str = self._stringify_storage()
        FileService.write(self._storage_filename, f"{updated_storage_str}\n")

    def _stringify_storage(self) -> str:
        return "\n".join(
            [
                f"{key}{KEY_VALUE_DELIMITER}{value}"
                for (key, value) in self._storage.items()
            ]
        )


def _split_by(delimiter: str) -> Callable[[str], list[str]]:
    def split_by_delimiter(string: str):
        return string.split(delimiter)

    return split_by_delimiter
