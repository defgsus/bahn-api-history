import pandas as pd
import numpy as np

from tqdm import tqdm
from src.changelog_reader import *
from src.filter import *


def parking_dataframe(
        per_snapshot: bool = False,
        with_name: bool = False,
        id_filter: StringFilter = None,
        date_filter: StringFilter = None,
) -> pd.DataFrame:
    rows = []

    changelog_files = ChangelogReader.get_changelog_files("parking")
    for fn in changelog_files:
        cl = ChangelogReader(*fn)
        for obj_id in tqdm(cl.object_ids(), desc=f"parsing {fn[0].name}"):
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
                    "valid": 0,
                }
                if data:
                    if with_name:
                        row["name"] = data["space"]["nameDisplay"]
                    alloc = data.get("allocation") or {}
                    if alloc.get("validData") and "category" in alloc:
                        row.update({
                            "valid": 1,
                            "category": alloc["category"],
                            "capacity": alloc["capacity"]
                        })
                rows.append(row)

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])

    index_columns = ["date", "id"]
    if with_name:
        index_columns += ["name"]

    return df.set_index(index_columns).sort_index()
