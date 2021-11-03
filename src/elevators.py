import pandas as pd
import numpy as np

from .changelog_reader import ChangelogReader


def elevators_dataframe() -> pd.DataFrame:
    rows = []

    changelog_files = ChangelogReader.get_changelog_files("elevators")
    for fn in changelog_files:
        cl = ChangelogReader(*fn)
        for obj_id in cl.object_ids():
            for dt, data in cl.iter_object(obj_id):
                if data:
                    rows.append({
                        "date": dt,
                        "id": obj_id,
                        "type": data["type"],
                        "station": str(data["stationnumber"]),
                        "active": 1 if data["state"] == "ACTIVE" else 0
                    })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index(["date", "id"]).sort_index()

