from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class PromptService:
    @staticmethod
    def text(text: str) -> str:
        return inquirer.text(text, amark="✔").execute()

    @staticmethod
    def confirm(text: str) -> bool:
        return inquirer.confirm(text).execute()

    @staticmethod
    def select[T](text: str, options: list[(T, str)], initial_value: T | None = None):
        choices = [Choice(value, label) for (value, label) in options]
        return inquirer.select(
            text,
            choices=choices,
            default=initial_value,
            max_height="100%",
        ).execute()
