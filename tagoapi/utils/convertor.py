from typing import TYPE_CHECKING, Union, Callable, TypeVar, Any
if TYPE_CHECKING:
    from tagoapi import TAGOClient
T = TypeVar('T', dict, list) # list, dict으로 매개변수 받을 때
U = TypeVar('U', dict[str], list) # list, dict으로 반환할 때

def convert(res: T, converter: Callable[[T, TAGOClient], U], _client: TAGOClient) -> U:
    if not res:
        return None
    return converter(res, _client)
