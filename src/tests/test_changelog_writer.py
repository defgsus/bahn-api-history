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

    def assert_equal(self, expected, real):
        self.assertEqual(
            expected, real,
            f"\n\nExpected: {json.dumps(expected, indent=2)}\n\nGot: {json.dumps(real, indent=2)}"
        )

    def assert_file(self, filename: Path, data: Union[dict, list]):
        real_data = json.loads(filename.read_text())
        self.assert_equal(data, real_data)

    def test_writer(self):
        writer = TestChangelogWriter()
        if writer.export_path.exists():
            shutil.rmtree(writer.export_path)

        for i in range(2):

            # second run will be an update of 2001
            writer.publish_files(PATH / "data")

            self.assert_file(
                writer.export_path / "2000-changelog.json",
                {
                    "1": [
                        {"date": "2000-01-01T00:00:00", "init": {"id": 1, "value": "a"}},
                        {"date": "2000-01-03T00:00:00", "not_listed": True}
                    ],
                    "2": [
                        {"date": "2000-01-01T00:00:00", "init": {"id": 2, "value": "b"}},
                        {"date": "2000-01-02T00:00:00", "changes": {"replace": [{"path": "value", "value": "b2"}]}}
                    ],
                    "3": [
                        {"date": "2000-01-04T00:00:00", "init": {"id": 3, "value": "c"}},
                    ]
                }
            )

            self.assert_file(
                writer.export_path / "2001-changelog.json",
                {
                    "1": [
                        {"date": "2001-01-01T00:00:00", "not_listed": True},
                        {"date": "2001-01-02T00:00:00", "init": {"id": 1, "value": "a"}}
                    ],
                    "2": [
                        {"date": "2001-01-01T00:00:00", "init": {"id": 2, "value": "b2"}},
                        {"date": "2001-01-01T00:00:00", "changes": {"replace": [{"path": "value", "value": "b3"}]}}
                    ],
                    "3": [
                        {"date": "2001-01-01T00:00:00", "init": {"id": 3, "value": "c"}},
                        {"date": "2001-01-01T00:00:00", "not_listed": True},
                        {"date": "2001-01-02T00:00:00", "init": {"id": 3, "value": "c"}},
                    ]
                }
            )

            self.assert_file(
                writer.export_path / "2000-dates.json",
                [
                    "2000-01-01T00:00:00",
                    "2000-01-02T00:00:00",
                    "2000-01-03T00:00:00",
                    "2000-01-04T00:00:00"
                ]
            )
            self.assert_file(
                writer.export_path / "2001-dates.json",
                [
                    "2001-01-01T00:00:00",
                    "2001-01-02T00:00:00"
                ]
            )

    def test_reader(self):
        writer = TestChangelogWriter()
        if writer.export_path.exists():
            shutil.rmtree(writer.export_path)

        writer.publish_files(PATH / "data")

        changelog_files = ChangelogReader.get_changelog_files(path=PATH / "export")
        self.assertEqual(2, len(changelog_files))

        self.assert_equal(
            [
                ("2000-01-01T00:00:00", {"id": 1, "value": "a"}),
                ("2000-01-03T00:00:00", None),
                ("2001-01-01T00:00:00", None),
                ("2001-01-02T00:00:00", {"id": 1, "value": "a"}),
            ],
            sum(
                list(
                    list(ChangelogReader(*f).iter_object("1"))
                    for f in changelog_files
                ), []
            )
        )

        self.assert_equal(
            [
                ("2000-01-01T00:00:00", {"id": 1, "value": "a"}),
                ("2000-01-02T00:00:00", {"id": 1, "value": "a"}),
                ("2000-01-03T00:00:00", None),
                ("2000-01-04T00:00:00", None),
                ("2001-01-01T00:00:00", None),
                ("2001-01-02T00:00:00", {"id": 1, "value": "a"}),
            ],
            sum(
                list(
                    list(ChangelogReader(*f).iter_object_snapshots("1"))
                    for f in changelog_files
                ), []
            )
        )

        self.assert_equal(
            [
                ("2000-01-01T00:00:00", {"id": 2, "value": "b"}),
                ("2000-01-02T00:00:00", {"id": 2, "value": "b2"}),
                ("2001-01-01T00:00:00", {"id": 2, "value": "b3"}),
            ],
            sum(
                list(
                    list(ChangelogReader(*f).iter_object("2"))
                    for f in changelog_files
                ), []
            )
        )

        self.assert_equal(
            [
                ("2000-01-01T00:00:00", {"id": 2, "value": "b"}),
                ("2000-01-02T00:00:00", {"id": 2, "value": "b2"}),
                ("2000-01-03T00:00:00", {"id": 2, "value": "b2"}),
                ("2000-01-04T00:00:00", {"id": 2, "value": "b2"}),
                ("2001-01-01T00:00:00", {"id": 2, "value": "b3"}),
                ("2001-01-02T00:00:00", {"id": 2, "value": "b3"}),
            ],
            sum(
                list(
                    list(ChangelogReader(*f).iter_object_snapshots("2"))
                    for f in changelog_files
                ), []
            )
        )

        self.assert_equal(
            [
                ("2000-01-04T00:00:00", {"id": 3, "value": "c"}),
                ("2001-01-01T00:00:00", None),
                ("2001-01-02T00:00:00", {"id": 3, "value": "c"}),
            ],
            sum(
                list(
                    list(ChangelogReader(*f).iter_object("3"))
                    for f in changelog_files
                ), []
            )
        )

        self.assert_equal(
            [
                ("2000-01-01T00:00:00", None),
                ("2000-01-02T00:00:00", None),
                ("2000-01-03T00:00:00", None),
                ("2000-01-04T00:00:00", {"id": 3, "value": "c"}),
                ("2001-01-01T00:00:00", None),
                ("2001-01-02T00:00:00", {"id": 3, "value": "c"}),
            ],
            sum(
                list(
                    list(ChangelogReader(*f).iter_object_snapshots("3"))
                    for f in changelog_files
                ), []
            )
        )


if __name__ == "__main__":
    unittest.main()
