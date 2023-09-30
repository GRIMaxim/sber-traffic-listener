from enum import Enum


class ErrorMessages(str, Enum):
    """Перечисление ответов для возникающих ошибок."""

    incorrect_links: str = "Links must be not empty and contains only links like 'http://examle.com/'"

    incorrect_parameters: str = "Parameter 'from' greatest 'to'"

    empty_result: str = "Domains not found"
