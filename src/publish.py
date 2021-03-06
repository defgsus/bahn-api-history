
from .changelog_writer import *


class ElevatorsChangelogWriter(ChangelogWriter):

    def __init__(self):
        super().__init__("elevators")

    @classmethod
    def get_object_list(cls, data: Union[dict, list]) -> List[dict]:
        return data

    @classmethod
    def get_object_id(cls, data: dict) -> str:
        return str(data["equipmentnumber"])


class ParkingChangelogWriter(ChangelogWriter):

    def __init__(self):
        super().__init__("parking")

    @classmethod
    def get_object_list(cls, data: Union[dict, list]) -> List[dict]:
        return data["allocations"]

    @classmethod
    def get_object_id(cls, data: dict) -> str:
        return str(data["space"]["id"])

    @classmethod
    def process_object(cls, data: dict) -> dict:
        data["allocation"].pop("timeSegment", None)
        data["allocation"].pop("timestamp", None)
        return data


class StationsChangelogWriter(ChangelogWriter):

    def __init__(self):
        super().__init__("stations")

    @classmethod
    def get_object_list(cls, data: Union[dict, list]) -> List[dict]:
        return data["result"]

    @classmethod
    def get_object_id(cls, data: dict) -> str:
        return str(data["number"])
