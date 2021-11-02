import argparse

from src.stations import StationsChangelogWriter
from src.elevators import ElevatorsChangelogWriter
from src.parking import ParkingChangelogWriter


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

    return parser.parse_args()


def main(args):
    if args.stations:
        StationsChangelogWriter().import_files(args.stations)

    if args.elevators:
        ElevatorsChangelogWriter().import_files(args.elevators)

    if args.parking:
        ParkingChangelogWriter().import_files(args.parking)


if __name__ == "__main__":
    main(parse_args())
