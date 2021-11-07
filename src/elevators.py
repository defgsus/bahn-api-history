from pathlib import Path
import hashlib
import os
import datetime

import dateutil.parser
import pandas as pd
import numpy as np
from tqdm import tqdm

from .changelog_reader import ChangelogReader
from .mapper import ObjectMapper
from .filter import *

CACHE_PATH = Path(__file__).resolve().parent.parent / "cache"


class ElevatorsMapper(ObjectMapper):

    IGNORE_FIELDS = ("state", "stateExplanation")

    def __init__(self):
        super().__init__("elevators")


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


def elevators_per_day(
        id_filter: StringFilter = None,
        date_filter: StringFilter = None,
        caching: Union[bool, str] = True,
) -> pd.DataFrame:
    from .stations import StationMapper
    station_mapper = StationMapper.singleton()

    param_hash = hashlib.md5(f"{id_filter} {date_filter}".encode("utf-8")).hexdigest()
    cache_file = CACHE_PATH / f"elevators-day-{param_hash}.pkl"

    changelog_files = ChangelogReader.get_changelog_files("elevators")

    if caching is True or caching == "read":
        if cache_file.exists() and cache_file.stat().st_mtime >= changelog_files[-1][0].stat().st_mtime:
            return pd.read_pickle(cache_file)

    rows = dict()
    objects_already_listed = set()

    for fn in changelog_files:
        cl = ChangelogReader(*fn)
        for obj_id in tqdm(cl.object_ids(), desc=f"parsing objects from {fn[0].name}"):
            if not filter_string(obj_id, id_filter):
                continue

            for dt, obj in cl.iter_object_snapshots(obj_id):
                if not filter_string(dt, date_filter):
                    continue

                if not obj and obj_id not in objects_already_listed:
                    continue
                objects_already_listed.add(obj_id)

                key = (dt[:10], obj_id)
                if key not in rows:
                    rows[key] = {
                        "snapshots": 0, "listed": 0, "active": 0, "inactive": 0,
                        "station_id": None, "station_name": None, "geo_coords": None,
                        "operator": None, "management": None, "zentrale": None,
                        "bearer": None, "region": None,
                        "state": None, "stepless": None, "price_category": None,
                    }
                row = rows[key]
                row["snapshots"] += 1
                if obj:
                    row["listed"] += 1

                    if not row["operator"]:
                        station = station_mapper(obj["stationnumber"])#, dt)
                        row.update({
                            "operator": obj.get("operatorname"),
                            "station_id": obj["stationnumber"],
                            "station_name": station.get("name"),
                            "state": station.get("federalState"),
                            "stepless": station.get("hasSteplessAccess"),
                            "management": station.get("stationManagement", {}).get("name"),
                            "zentrale": station.get("szentrale", {}).get("name"),
                            "bearer": station.get("aufgabentraeger", {}).get("name"),
                            "region": station.get("regionalbereich", {}).get("name"),
                            "price_category": station.get("priceCategory"),
                        })
                    if not row["geo_coords"] and obj.get("geocoordX") and obj.get("geocoordY"):
                        row["geo_coords"] = (obj["geocoordX"], obj["geocoordY"])

                    if obj["state"] == "ACTIVE":
                        row["active"] += 1
                    else:
                        row["inactive"] += 1

    columns = list(rows[next(iter(rows))].keys())
    rows = [
        [key[0], key[1]] + [row[c] for c in columns]
        for key, row in rows.items()
    ]
    df = pd.DataFrame(rows, columns=["date", "id"] + columns)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index(["date", "id"], inplace=True)

    if caching is True or caching == "write":
        os.makedirs(CACHE_PATH, exist_ok=True)
        df.to_pickle(cache_file)

    return df

