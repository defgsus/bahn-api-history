import argparse
from pathlib import Path

from src.publish import (
    StationsChangelogWriter, ElevatorsChangelogWriter, ParkingChangelogWriter
)
from src.summary import summary


PATH = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stations", type=str, nargs="?",
        help="Path to stations snapshots",
    )
    parser.add_argument(
        "--elevators", type=str, nargs="?",
        help="Path to elevators snapshots",
    )
    parser.add_argument(
        "--parking", type=str, nargs="?",
        help="Path to parking snapshots",
    )
    parser.add_argument(
        "--readme", type=bool, nargs="?", default=False, const=True,
        help="Render new README.md",
    )

    return parser.parse_args()


def render_readme():
    markdown = (PATH / "templates" / "README.md").read_text()

    markdown = markdown % {
        "summary_parking": summary("parking"),
        "summary_elevators": summary("elevators"),
        "summary_stations": summary("stations"),
    }

    (PATH / "README.md").write_text(markdown)


def main(args):
    if args.stations:
        StationsChangelogWriter().publish_files(args.stations)

    if args.elevators:
        ElevatorsChangelogWriter().publish_files(args.elevators)

    if args.parking:
        ParkingChangelogWriter().publish_files(args.parking)

    if args.readme:
        render_readme()


if __name__ == "__main__":
    main(parse_args())
