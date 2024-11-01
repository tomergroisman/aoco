import os
import shutil
from pathlib import Path


class FileService:
    @staticmethod
    def create_dir_gracefully(path: str) -> None:
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_file_gracefully(filename: str) -> None:
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
    def mkdir(path: str) -> None:
        os.makedirs(path)

    @staticmethod
    def is_dir_exists(path: str) -> bool:
        return Path(path).is_dir()

    @staticmethod
    def is_file_exists(filename: str) -> bool:
        return Path(filename).is_file()

    @staticmethod
    def dir_content(path: str) -> list[str]:
        return [filename.name for filename in Path(path).iterdir()]
