from pathlib import Path
import json
import os
import glob
import datetime
import dateutil.parser
import pytz
from typing import Union, Generator, Tuple, List, Optional

from tqdm import tqdm

from .compare import compare
from .changelog_reader import ChangelogReader


class ChangelogWriter:

    def __init__(self, type: str):
        self.type = type
        self.export_path = Path(__file__).resolve().parent.parent / "docs" / "data" / self.type

    @classmethod
    def get_object_list(cls, data: Union[dict, list]) -> List[dict]:
        raise NotImplementedError

    @classmethod
    def get_object_id(cls, data: dict) -> str:
        raise NotImplementedError

    @classmethod
    def get_date_bucket(cls, dt: datetime.datetime) -> str:
        return dt.strftime("%Y")

    @classmethod
    def bucket_to_date(cls, s: str) -> datetime:
        return datetime.datetime.strptime(s, "%Y")

    @classmethod
    def process_object(cls, data: dict) -> dict:
        return data

    @classmethod
    def iter_snapshot_files(
            cls,
            path: Union[str, Path],
            tqdm_desc: Optional[str] = None,
            min_date: Optional[datetime.datetime] = None,
    ) -> Generator[Tuple[datetime.datetime, Union[dict, list]], None, None]:
        path = Path(path)
        for fn in tqdm(
                sorted(glob.glob(str(path / "*.json"), recursive=True)),
                desc=tqdm_desc,
        ):
            fn = Path(fn)
            timestamp = fn.name[:25]
            if timestamp.endswith(".json"):
                timestamp = timestamp[:-5]
            try:
                dt = (
                    dateutil.parser.parse(timestamp)
                    .astimezone(pytz.utc).replace(tzinfo=None)
                )
            except dateutil.parser.ParserError:
                continue

            if min_date and dt < min_date:
                continue

            try:
                text = fn.read_text()
            except UnicodeDecodeError as e:
                #raise UnicodeError(f"{e} in {fn}: {e.object[:1000]}")
                print(f"{type(e).__name__} {e}: in {fn}")
                continue

            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                print(f"{type(e).__name__} {e}: in {fn}")
                continue

            if isinstance(data, dict) and "error" in data:
                continue

            yield dt, data

    @classmethod
    def sorted_object(cls, data: Union[dict, list, tuple]) -> Union[list, dict]:
        if isinstance(data, (tuple, list)):
            return [
                cls.sorted_object(o) if isinstance(o, (tuple, list, dict)) else o
                for o in data
            ]
        assert isinstance(data, dict)
        sorted_data = {}
        for key in sorted(data.keys()):
            value = data[key]
            if isinstance(value, (tuple, list, dict)):
                value = cls.sorted_object(value)
            sorted_data[key] = value
        return sorted_data

    def get_changelog_files(self) -> List[Path]:
        return sorted(
            Path(f)
            for f in glob.glob(str(self.export_path / "*.json"), recursive=True)
            if not f.endswith("-snapshots.json")
        )

    def publish_files(self, path: Union[str, Path]):
        path = Path(path)

        objects = dict()
        unlisted_object_ids = set()
        changelog = dict()
        snapshot_dates = []
        previous_date_bucket = None

        min_date = None
        changelog_files = self.get_changelog_files()
        if changelog_files:
            min_date = self.bucket_to_date(changelog_files[-1].name[:-5])
            if len(changelog_files) > 1:
                print("reading", changelog_files[-2])
                cl = ChangelogReader(changelog_files[-2])
                objects = {
                    obj_id: cl.object(obj_id)
                    for obj_id in cl.object_ids()
                }
                unlisted_object_ids = set(obj_id for obj_id, obj in objects.items() if obj is None)

        for dt, data in self.iter_snapshot_files(
                path, min_date=min_date, tqdm_desc=f"{path.name} >= {min_date}"
        ):
            data = self.sorted_object(data)
            snapshot_dates.append(dt.isoformat())

            date_bucket = self.get_date_bucket(dt)
            if date_bucket != previous_date_bucket:
                if changelog:
                    os.makedirs(self.export_path, exist_ok=True)
                    self.store_changelog(self.export_path / f"{previous_date_bucket}", changelog, snapshot_dates)

                # reset log
                snapshot_dates = []
                changelog = {
                    obj_id: [{
                        "date": dt.isoformat(),
                        **(
                            {"init": objects[obj_id]}
                            if obj_id not in unlisted_object_ids else
                            {"not_listed": True}
                        ),
                    }]
                    for obj_id in set(objects.keys()) | unlisted_object_ids
                }
            previous_date_bucket = date_bucket

            previous_object_ids = set(obj_id for obj_id, obj in objects.items() if obj is not None)

            for obj_data in self.get_object_list(data):
                obj_data = self.process_object(obj_data)

                obj_id = self.get_object_id(obj_data)

                if obj_id in previous_object_ids:
                    previous_object_ids.remove(obj_id)

                if objects.get(obj_id) is None:
                    print("NEW", obj_id)
                    objects[obj_id] = obj_data
                    if obj_id in unlisted_object_ids:
                        unlisted_object_ids.remove(obj_id)
                    changelog.setdefault(obj_id, []).append({
                        "date": dt.isoformat(),
                        "init": obj_data,
                    })

                else:
                    changes = compare(objects[obj_id], obj_data)
                    objects[obj_id] = obj_data
                    if changes:
                        changelog[obj_id].append({
                            "date": dt.isoformat(),
                            "changes": changes,
                        })

            for obj_id in previous_object_ids:
                changelog[obj_id].append({
                    "date": dt.isoformat(),
                    "not_listed": True,
                })
                print("NOT LISTED", obj_id)
                del objects[obj_id]
                unlisted_object_ids.add(obj_id)

        if changelog:
            os.makedirs(self.export_path, exist_ok=True)
            self.store_changelog(self.export_path / f"{previous_date_bucket}", changelog, snapshot_dates)

    @classmethod
    def store_changelog(cls, filename: Union[str, Path], export_data: dict, snapshot_dates: List[str]):
        export_data = cls.sorted_object(export_data)

        print("writing", str(filename) + ".json")
        with open(str(filename) + ".json", "wt") as fp:
            print("{", file=fp)
            for i, obj_id in enumerate(sorted(export_data)):
                print(f'  "{obj_id}": [', file=fp)
                for j, change in enumerate(export_data[obj_id]):
                    comma = "," if j+1 < len(export_data[obj_id]) else ""
                    print(f'    {json.dumps(change,)}{comma}', file=fp)

                comma = "," if i+1 < len(export_data) else ""
                print(f'  ]{comma}', file=fp)
            print("}", file=fp)

        print("writing", str(filename) + "-snapshots.json")
        with open(str(filename) + "-snapshots.json", "wt") as fp:
            json.dump(sorted(snapshot_dates), fp, indent=2)

