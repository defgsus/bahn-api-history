import fnmatch
from typing import Optional, Union, Sequence, Callable


StringFilter = Optional[Union[str, Sequence[str], Callable[[str], bool]]]


def filter_string(s: str, f: StringFilter) -> bool:
    if f is None:
        return True
    if isinstance(f, str):
        return fnmatch.fnmatchcase(s, f)
    elif isinstance(f, Sequence):
        return any(fnmatch.fnmatchcase(s, x) for x in f)
    elif callable(f):
        return f(s)
    else:
        raise TypeError(f"Invalid string filter type '{type(f).__name__}'")
