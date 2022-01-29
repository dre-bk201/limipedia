from typing import Any, List, Tuple, Union


class SafeList(list):
    def __init__(self, *args, **kwargs):
        super(SafeList, self).__init__(*args, **kwargs)

    def __getitem__(self, key: int):
        return super(SafeList, self).__getitem__(key)

    def __setitem__(self, key: int, item: Any):
        super(SafeList, self).__setitem__(key, item)

    def get(self, index: int) -> Union[int, None]:
        try:
            return self[index]
        except:
            return None


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
