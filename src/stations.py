from typing import Optional

from .changelog_reader import ChangelogReader


class StationMapper:

    def __init__(self):
        self._station_map = dict()

    def __getitem__(self, station_number: str) -> Optional[dict]:
        if not self._station_map:
            self._load_stations()

        return self._station_map.get(station_number)

    def _load_stations(self):
        changelog_files = ChangelogReader.get_changelog_files("stations")
        for fn in changelog_files:
            cl = ChangelogReader(*fn)
            for obj_id in cl.object_ids():

                if obj_id not in self._station_map:
                    for dt, obj in cl.iter_object(obj_id):
                        if obj:
                            self._station_map[obj_id] = obj
                            break
