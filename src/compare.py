from typing import List, Union, Tuple, Any, Dict, Optional


class _UNSET:
    pass


class Comparer:

    def __init__(self, data1: dict, data2: dict):
        self.changes = dict()
        self._compare(data1, data2, [])

    def _compare(self, value_self: Any, value_other: Any, path: List[str]):
        type_self, type_other = type(value_self), type(value_other)
        if type_self != type_other:
            self._log("replace", path, value_other)
            return

        if isinstance(value_self, dict):
            if value_self != value_other:
                self._compare_dict(value_self, value_other, path)

        elif isinstance(value_self, (list, tuple)):
            if len(value_self) != len(value_other):
                self._log("replace", path, value_other)
            else:
                for i in range(len(value_self)):
                    self._compare(value_self[i], value_other[i], path + [str(i)])
        else:
            if value_self != value_other:
                # print("REPLACE", path, value_self, "#", value_other)
                self._log("replace", path, value_other)

    def _compare_dict(self, data_self: dict, data_other: dict, path: List[str]):
        assert isinstance(data_self, dict)
        for key in sorted(set(data_self) | set(data_other)):
            if key not in data_other:
                self._log("remove", path + [key])
                continue

            if key not in data_self:
                self._log("add", path + [key], data_other[key])
                continue

            self._compare(data_self[key], data_other[key], path + [key])

    def _log(self, action: str, path: List[str], value=_UNSET):
        if action not in self.changes:
            self.changes[action] = []
        entry = {"path": ".".join(path)}
        if value is not _UNSET:
            entry["value"] = value
        self.changes[action].append(entry)


def compare(data1: dict, data2: dict) -> Dict[str, List[dict]]:
    return Comparer(data1, data2).changes
