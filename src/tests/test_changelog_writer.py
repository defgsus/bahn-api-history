import unittest
import shutil

from src.changelog_writer import *

PATH = Path(__file__).resolve().parent


class TestChangelogWriter(ChangelogWriter):

    def __init__(self):
        super().__init__(PATH / "export")

    @classmethod
    def get_object_list(cls, data: Union[dict, list]) -> List[dict]:
        return data

    @classmethod
    def get_object_id(cls, data: dict) -> str:
        return str(data["id"])


class TestTheChangelogWriter(unittest.TestCase):

    def assert_file(self, filename: Path, data: dict):
        real_data = json.loads(filename.read_text())
        self.assertEqual(
            data, real_data,
            f"\n\nExpected: {json.dumps(data, indent=2)}\n\nGot: {json.dumps(real_data, indent=2)}"
        )

    def test_writer(self):
        writer = TestChangelogWriter()
        if writer.export_path.exists():
            shutil.rmtree(writer.export_path)

        for i in range(2):
            # second time will be an update of 2001
            writer.publish_files(PATH / "data")

            self.assert_file(
                writer.export_path / "2000.json",
                {
                    "1": [
                        {"date": "2000-01-01T00:00:00", "init": {"id": 1, "value": "a"}},
                        {"date": "2000-01-03T00:00:00", "not_listed": True}
                    ],
                    "2": [
                        {"date": "2000-01-01T00:00:00", "init": {"id": 2, "value": "b"}},
                        {"date": "2000-01-02T00:00:00", "changes": {"replace": [{"path": "value", "value": "b2"}]}}
                    ]
                }
            )

            self.assert_file(
                writer.export_path / "2001.json",
                {
                    "1": [
                        {"date": "2001-01-01T00:00:00", "not_listed": True},
                        {"date": "2001-01-02T00:00:00", "init": {"id": 1, "value": "a"}}
                    ],
                    "2": [
                        {"date": "2001-01-01T00:00:00", "init": {"id": 2, "value": "b2"}},
                        {"date": "2001-01-01T00:00:00", "changes": {"replace": [{"path": "value", "value": "b3"}]}}
                    ]
                }
            )


if __name__ == "__main__":
    unittest.main()
