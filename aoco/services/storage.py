from typing import Callable, TextIO

from aoco.constants import KEY_VALUE_DELIMITER


class StorageService:
    def __init__(self, storage_filename: str) -> None:
        self._storage_filename = storage_filename
        self._create_storage_file_if_not_exists()
        self._storage = self._create_storage_from_storage_file()

    def get(self, key: str) -> str | None:
        return self._storage.get(key)

    def set(self, key: str, value: str) -> None:
        self._storage.update({key: value})
        self._update_storage_file()

    def _open_storage_file_for_read(self) -> TextIO:
        return open(self._storage_filename, "r")

    def _open_storage_file_for_write(self) -> TextIO:
        return open(self._storage_filename, "w")

    def _create_storage_file_if_not_exists(self) -> None:
        storage_file = open(self._storage_filename, "a+")
        storage_file.close()

    def _create_storage_from_storage_file(self) -> dict[str, str]:
        storage_file = self._open_storage_file_for_read()
        storage_str = storage_file.read()
        storage_file.close()
        storage_rows = storage_str.split("\n")[:-1]
        return {
            key: value
            for [key, value] in map(_split_by(KEY_VALUE_DELIMITER), storage_rows)
        }

    def _update_storage_file(self) -> None:
        updated_storage_str = self._stringify_storage()
        storage_file = self._open_storage_file_for_write()
        storage_file.write(f"{updated_storage_str}\n")
        storage_file.close()

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
