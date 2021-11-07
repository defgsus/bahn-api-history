from pathlib import Path
import glob
import sys

import pandas as pd

from .changelog_reader import ChangelogReader
from .stations import StationMapper


def summary(object_type: str) -> str:
    num_snapshots = 0
    num_changes = dict()
    objects = dict()
    min_date, max_date = None, None
    stations = StationMapper()

    changelog_files = ChangelogReader.get_changelog_files(object_type)

    for fn in changelog_files:
        print("reading", fn[0], file=sys.stderr)
        cl = ChangelogReader(*fn)
        num_snapshots += len(cl.dates)

        for obj_id, changelog in cl.data.items():
            num_changes[obj_id] = num_changes.get(obj_id, 0) + len(changelog)
            if min_date is None or min_date > changelog[0]["date"]:
                min_date = changelog[0]["date"]
            if max_date is None or max_date < changelog[-1]["date"]:
                max_date = changelog[-1]["date"]

            if obj_id not in objects:
                for dt, data in cl.iter_object(obj_id):
                    if data:
                        objects[obj_id] = data
                        break

    top_ids = sorted(num_changes, key=lambda k: num_changes[k], reverse=True)[:10]

    md = f"**{len(num_changes):,}** objects" \
         f", **{num_snapshots:,}** snapshots" \
         f", **{sum(num_changes.values()):,}** changes" \
         f" ({min_date.replace('T', ' ')} - {max_date.replace('T', ' ')})" \
         f"\n\n"

    rows = []
    for obj_id in top_ids:
        data = objects[obj_id]
        if object_type == "parking":
            name = data["space"]["nameDisplay"]
        elif object_type == "elevators":
            name = str(data["stationnumber"])
            station = stations[name]
            if station:
                name = station["name"]
            name += " " + data["type"] + " " + data["description"]
        elif object_type == "stations":
            name = data["name"]

        rows.append({
            "id": obj_id,
            "name": name,
            "num changes": num_changes[obj_id],
        })

    md += pd.DataFrame(rows).set_index("id").to_markdown()

    return md

