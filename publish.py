import argparse
from pathlib import Path
from multiprocessing import Process

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
    procs = []

    if args.stations:
        procs.append(Process(target=lambda : StationsChangelogWriter().publish_files(args.stations)))

    if args.elevators:
        procs.append(Process(target=lambda : ElevatorsChangelogWriter().publish_files(args.elevators)))

    if args.parking:
        procs.append(Process(target=lambda : ParkingChangelogWriter().publish_files(args.parking)))

    if procs:
        [t.start() for t in procs]
        [t.join() for t in procs]

    if args.readme:
        render_readme()


if __name__ == "__main__":
    main(parse_args())
