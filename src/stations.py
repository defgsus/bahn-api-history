
from .changelog_writer import *


class StationsChangelogWriter(ChangelogWriter):

    def __init__(self):
        super().__init__("stations")

    @classmethod
    def get_object_list(cls, data: Union[dict, list]) -> List[dict]:
        return data["result"]

    @classmethod
    def get_object_id(cls, data: dict) -> str:
        return str(data["number"])
