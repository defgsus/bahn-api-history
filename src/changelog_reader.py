from pathlib import Path
import json
import datetime
import dateutil.parser
from copy import deepcopy
from typing import Union, Generator, Tuple, List, Optional


class ChangelogReader:

    def __init__(self, filename: Union[str, Path]):
        self.filename = Path(filename)
        self.data = json.loads(self.filename.read_text())

    def object_ids(self) -> Generator[str, None, None]:
        return self.data.keys()

    def snapshot_dates(self, obj_id: str) -> List[datetime.datetime]:
        changelog = self.data[obj_id]
        return [e["date"] for e in changelog]

    def object(self, obj_id: str, at: Optional[datetime.datetime] = None) -> Optional[dict]:
        if at:
            at = at.isoformat()

        cur_data = None
        for dt, data in self.iter_object(obj_id):

            if at and dt > at:
                return cur_data

            cur_data = data

        return cur_data

    def iter_object(self, obj_id: str) -> Generator[Tuple[str, Optional[dict]], None, None]:
        cur_data = None
        for changelog in self.data[obj_id]:
            dt = changelog["date"]

            for change_key in changelog:
                if change_key == "date":
                    continue

                elif change_key == "init":
                    cur_data = deepcopy(changelog["init"])

                elif change_key == "not_listed":
                    cur_data = None

                elif change_key == "changes":
                    try:
                        changes = changelog["changes"]
                        assert cur_data, f"cur_data not present for 'changes' entry '{obj_id}' @ {dt}"
                        for change_type in changes.keys():
                            if change_type == "add":
                                for entry in changes[change_type]:
                                    self._add_object_value(cur_data, entry["path"], entry["value"])

                            elif change_type == "remove":
                                for entry in changes[change_type]:
                                    self._remove_object_value(cur_data, entry["path"])

                            elif change_type == "replace":
                                for entry in changes[change_type]:
                                    self._set_object_value(cur_data, entry["path"], entry["value"])

                            else:
                                raise ValueError(f"Unhandled change-type '{change_type}'")

                    except Exception as e:
                        raise Exception(f"{e}\n\n{obj_id}: changelog: {changelog}")

                else:
                    raise ValueError(f"Unhandled change-key '{change_key}'")

            yield dt, cur_data

    def _get_sub_object(self, data: dict, path: Union[str, List[str]]):
        obj = data
        if isinstance(path, str):
            cur_path = path.split(".")
        else:
            cur_path = path
        while cur_path:
            key = cur_path[0]
            if isinstance(obj, dict):
                pass
            elif isinstance(obj, list):
                key = int(key)
            else:
                raise TypeError(f"Can not descend into {type(obj).__name__} with {path}")

            try:
                obj = obj[key]
            except KeyError:
                raise KeyError(f"'{key}' {path} in {data}")

            cur_path.pop(0)
        return obj

    def _set_object_value(self, data: dict, path: str, value):
        assert path
        path = path.split(".")
        obj = self._get_sub_object(data, path[:-1])
        key = path[-1]
        if isinstance(obj, dict):
            pass
        elif isinstance(obj, list):
            key = int(key)
        else:
            raise TypeError(f"Can not descend into {type(obj).__name__} with '{key}' {path}")

        obj[key] = value

    def _add_object_value(self, data: dict, path: str, value):
        assert path
        path = path.split(".")
        obj = self._get_sub_object(data, path[:-1])
        key = path[-1]
        if isinstance(obj, dict):
            pass
        #elif isinstance(obj, list):
        #    key = int(key)
        else:
            raise TypeError(f"Can not descend into {type(obj).__name__} with '{key}' {path}")

        obj[key] = value

    def _remove_object_value(self, data: dict, path: str):
        assert path
        path = path.split(".")
        obj = self._get_sub_object(data, path[:-1])
        key = path[-1]
        if isinstance(obj, dict):
            del obj[key]
        #elif isinstance(obj, list):
        #    key = int(key)
        else:
            raise TypeError(f"Can not descend into {type(obj).__name__} with '{key}' {path}")

