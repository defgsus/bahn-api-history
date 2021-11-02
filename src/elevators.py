
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
