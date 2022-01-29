import hashlib
import json

from typing import Any, Dict, Iterable, List, Optional, SupportsIndex, Tuple, Union, overload


class SafeList(List[Any]):
    def __init__(self, *args, **kwargs):
        super(SafeList, self).__init__(*args, **kwargs)

    @overload
    def __getitem__(self, idx: SupportsIndex) -> Any: ...

    @overload
    def __getitem__(self, s: slice) -> List[Any]: ...

    def __getitem__(self, key):
        return super().__getitem__(key)

    @overload
    def __setitem__(self, index: SupportsIndex, item: Any) -> None: ...

    @overload
    def __setitem__(self, s: slice, x: Iterable[Any]) -> None: ...

    def __setitem__(self, key, item):
        super(SafeList, self).__setitem__(key, item)

    def get(self, index: int) -> Union[Any, None]:
        try:
            return self[index]
        except:
            return None

    def set(self, index: int, item: Any) -> bool:
        if self.get(index):
            self.__setitem__(index, item)
            return True
        return False


def group_as(arr: List[Any], group: int = 0) -> Union[List[Any], List[Tuple[Any]]]:
    new_list = []
    i = 0
    if group == 0:
        return arr
    else:
        low = 0
        high = group
        while i < len(arr) / group:
            new_list.append(tuple(arr[low:high]))
            low += group
            high += group
            i += 1

    return new_list


def uid(text: str) -> int:
    return int(str(int(hashlib.md5(text.encode()).hexdigest(), 16))[0:12])


def jsonify(item: Union[Dict[str, Any], List[Any]], indent: int = 4):
    print(json.dumps(item, indent=indent))
