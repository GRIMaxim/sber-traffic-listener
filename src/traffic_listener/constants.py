from enum import Enum


class ErrorMessages(str, Enum):
    """Перечисление ответов для возникающих ошибок."""

    list_is_empty: str = "Links must be not empty"
    list_contains_only_words: str = "Links must be contains a link like 'https://www.example.com/1'"

    incorrect_parameters: str = "Parameter 'from' greatest 'to'"
