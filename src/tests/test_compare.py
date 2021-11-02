import unittest

from src.compare import compare


class TestCompare(unittest.TestCase):

    def test_add(self):
        self.assertEqual(
            {
                "add": [{"path": "a", "value": 1}],
            },
            compare({}, {"a": 1})
        )
        self.assertEqual(
            {
                "add": [{"path": "b", "value": 2}, {"path": "c", "value": 3}],
            },
            compare({"a": 1}, {"a": 1, "b": 2, "c": 3})
        )

    def test_remove(self):
        self.assertEqual(
            {
                "add": [{"path": "b", "value": 1}],
                "remove": [{"path": "a"}],
            },
            compare({"a": 1}, {"b": 1})
        )

    def test_replace(self):
        self.assertEqual(
            {
                "replace": [{"path": "a", "value": 2}],
            },
            compare({"a": 1}, {"a": 2})
        )
        self.assertEqual(
            {
                "replace": [{"path": "a.b", "value": 2}],
            },
            compare({"a": {"b": 1}}, {"a": {"b": 2}})
        )


if __name__ == "__main__":
    unittest.main()
