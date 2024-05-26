import os
import typing
from typing import Any, Callable, List, Optional, TypeVar

T = TypeVar("T")  # Generic type
LIST = TypeVar(
    "LIST", list, typing.List
)  # Needs two args - typing.List is just an alias so I'm using that (hack)


def safe_list(value: Optional[LIST]) -> LIST:
    if value is None:
        return []
    else:
        return value


def map_list(original_list: List[Any], transform: Callable[[Any], Any]) -> List[Any]:
    return list(map(lambda list_item: transform(list_item), original_list))


def double_backslash_to_slash(text: str) -> str:
    return text.replace("\\", "/")


def string_contains(string: str, chars: str) -> bool:
    return string.find(chars) != -1


def string_contains_any(string: str, words: List[str]) -> bool:
    for word in words:
        if string_contains(string, word):
            return True

    return False


def list_is_not_empty(list: List) -> bool:
    return not list_is_empty(list)


def list_is_empty(list: List) -> bool:
    return len(list) == 0


def items_within_directory(directory: str) -> List[str]:
    return os.listdir(directory)
