import shutil
from typing import TextIO


class FileService:
    @staticmethod
    def create_gracefully(filename: str) -> None:
        storage_file = open(filename, "a+")
        storage_file.close()

    @staticmethod
    def read(filename: str) -> str:
        file = open(filename, "r")
        file_str = file.read()
        file.close()
        return file_str

    @staticmethod
    def write(filename: str, data: str) -> None:
        file = open(filename, "w")
        file.write(data)
        file.close()

    @staticmethod
    def copy(source: str, target: str) -> None:
        shutil.copy(source, target)

    @staticmethod
    def copy_tree(source: str, target: str) -> None:
        shutil.copytree(source, target, dirs_exist_ok=True)

    @staticmethod
    def _open_file_for_write(filename: str) -> TextIO:
        return open(filename, "w")
