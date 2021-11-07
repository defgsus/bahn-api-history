import datetime

import dateutil.parser

from .changelog_reader import ChangelogReader
from .filter import *


class ObjectMapper:

    IGNORE_FIELDS = tuple()
    DEFAULT = dict()

    __singleton = None

    @classmethod
    def singleton(cls) -> "ObjectMapper":
        if cls is ObjectMapper:
            raise TypeError(f"Only derived classes can be singleton-instanced")
        if not cls.__singleton:
            cls.__singleton = cls()  # derived classes
        return cls.__singleton

    def __init__(self, object_type: str):
        self._object_date_map = dict()
        self._object_map = dict()
        self.object_type = object_type

    def __getitem__(self, obj_id: str) -> dict:
        """
        Return first listed entry
        :return: dict or None
        """
        if not self._object_date_map:
            self._load_objects()

        object = self._object_map.get(str(obj_id))
        if not object:
            return self.DEFAULT
        return object

    def __call__(self, obj_id: str, date: Optional[Union[str, datetime.datetime]] = None) -> dict:
        """
        Return entry at specific time.

        :param obj_id: str
        :param date: str or datetime or None, If None return first valid entry
        :return: dict or DEFAULT
        """
        if not self._object_date_map:
            self._load_objects()

        if date is None:
            return self._object_map.get(str(obj_id)) or self.DEFAULT

        objects = self._object_date_map.get(str(obj_id))
        if not objects:
            return self.DEFAULT

        if not isinstance(date, str):
            date = str(date)

        if date < objects[0][0]:
            return self.DEFAULT
        if date > objects[-1][0]:
            return objects[-1][1]

        prev_obj = self.DEFAULT
        for dt, obj in objects:
            if dt >= date:
                return prev_obj
            prev_obj = obj
        return prev_obj

    def _load_objects(self):
        changelog_files = ChangelogReader.get_changelog_files(self.object_type)
        for fn in changelog_files:
            cl = ChangelogReader(*fn)
            for obj_id in cl.object_ids():

                prev_obj = None
                for dt, obj in cl.iter_object(obj_id):
                    if obj:
                        for field in self.IGNORE_FIELDS:
                            obj.pop(field, None)

                        if obj_id not in self._object_map:
                            self._object_map[obj_id] = obj

                        if obj != prev_obj:
                            if obj_id not in self._object_date_map:
                                self._object_date_map[obj_id] = []
                            self._object_date_map[obj_id].append((dt, obj))

                        prev_obj = obj
