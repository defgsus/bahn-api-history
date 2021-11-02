
from .changelog_writer import *


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
