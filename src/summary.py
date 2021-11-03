from pathlib import Path
import glob
import sys

import pandas as pd

from .changelog_reader import ChangelogReader
from .stations import StationMapper


def summary(object_type: str) -> str:
    num_changes = dict()
    objects = dict()
    stations = StationMapper()

    path = Path(__file__).resolve().parent.parent / "docs" / "data" / object_type
    changelog_files = sorted(glob.glob(str(path / "*.json")))
    for fn in changelog_files:
        print("reading", fn, file=sys.stderr)
        cl = ChangelogReader(fn)

        for obj_id, changelog in cl.data.items():
            num_changes[obj_id] = num_changes.get(obj_id, 0) + len(changelog)
            if obj_id not in objects:
                for dt, data in cl.iter_object(obj_id):
                    if data:
                        objects[obj_id] = data
                        break

    top_ids = sorted(num_changes, key=lambda k: num_changes[k], reverse=True)[:10]

    md = f"{len(num_changes)} objects, {sum(num_changes.values())} changes\n\n"

    rows = []
    for obj_id in top_ids:
        data = objects[obj_id]
        if object_type == "parking":
            name = data["space"]["title"]
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

