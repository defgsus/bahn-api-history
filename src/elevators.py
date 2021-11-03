import pandas as pd
import numpy as np

from .changelog_reader import ChangelogReader
from .filter import *


def elevators_dataframe(
        per_snapshot: bool = False,
        id_filter: StringFilter = None,
        date_filter: StringFilter = None,
) -> pd.DataFrame:
    rows = []

    changelog_files = ChangelogReader.get_changelog_files("elevators")
    for fn in changelog_files:
        cl = ChangelogReader(*fn)
        for obj_id in cl.object_ids():
            if not filter_string(obj_id, id_filter):
                continue

            if per_snapshot:
                object_iter = cl.iter_object_snapshots(obj_id)
            else:
                object_iter = cl.iter_object(obj_id)

            for dt, data in object_iter:
                if not filter_string(dt, date_filter):
                    continue

                row = {
                    "date": dt,
                    "id": obj_id,
                    "listed": 1 if data else 0,
                }
                if data:
                    row.update({
                        "type": data["type"],
                        "station": str(data["stationnumber"]),
                        "active": 1 if data["state"] == "ACTIVE" else 0
                    })
                rows.append(row)

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index(["date", "id"]).sort_index()

