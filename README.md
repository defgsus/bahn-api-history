# Deutsche Bahn API History

There was this [monumental talk](https://media.ccc.de/v/36c3-10652-bahnmining_-_punktlichkeit_ist_eine_zier)
in late 2019 about the *correctness* of the punctuality statistics published by
Deutsche Bahn, which got me interested in [api.deutschebahn.com](https://api.deutschebahn.com).

This repo contains non of the train schedule data. Instead it has change-logs of the
[parking api](https://developer.deutschebahn.com/store/apis/info?name=BahnPark&version=v1&provider=DBOpenData),
[station data api](https://developer.deutschebahn.com/store/apis/info?name=StaDa-Station_Data&version=v2&provider=DBOpenData)
and the [station facilities status api](https://developer.deutschebahn.com/store/apis/info?name=FaSta-Station_Facilities_Status&version=v2&provider=DBOpenData)
(status of elevators and escalators).

Since late January 2020 these APIs are sampled with separate cronjobs running
these shell commands:
```shell script
# parking
curl -X GET --header "Accept: application/json" \
    --header "Authorization: Bearer <YOUR_API_TOKEN>" \
    "https://api.deutschebahn.com/bahnpark/v1/spaces/occupancies" \
    > `date -Is -u`.json

# stations
curl -X GET --header "Accept: application/json" \
    --header "Authorization: Bearer <YOUR_API_TOKEN>" \
    "https://api.deutschebahn.com/stada/v2/stations?searchstring=*" \
    > `date -Is -u`.json

# elevators
curl -X GET --header "Accept: application/json" \
    --header "Authorization: Bearer <YOUR_API_TOKEN>" \
    "https://api.deutschebahn.com/fasta/v2/facilities?type=ESCALATOR,ELEVATOR"
    > `date -Is -u`.json
```

The changelogs are collected in json files per year in [docs/data/](docs/data) 
using a self-baked format which does not contain too much space and allows committing 
new json lines with minimal diffs. 

To get access to all objects via python:
```python
from src.changelog_reader import ChangelogReader

for changelog_file, dates_file in ChangelogReader.get_changelog_files("stations"):
    reader = ChangelogReader(changelog_file, dates_file)
    for object_id in reader.object_ids():
        for timestamp, data in reader.iter_object(object_id):
            print(f"object {object_id} at time {timestamp} is {data}")
```

If an object was not listed during a snapshot, `data` will be None. 

The `reader.iter_object(object_id)` method iterates through all changes of the 
object. The `reader.iter_object_snapshots(object_id)` method iterates through 
each snapshot regardless if the object is changed or does not yet exist.


## Summary

### free parking lots
 
50 objects, 48766 snapshots, 38012 changes

|     id | name                                                                                |   num changes |
|-------:|:------------------------------------------------------------------------------------|--------------:|
| 100054 | Düren P1 Düren P1 Parkplatz Ludwig-Erhardt-Platz                                    |          4068 |
| 100084 | Frankfurt (Main) Hbf P4 Frankfurt (Main) Hbf Bustasche                              |          3412 |
| 100201 | Mainz Hbf P3 Mainz Hbf P3 Tiefgarage Bonifazius-Türme UG -1                         |          3223 |
| 100083 | Frankfurt (Main) Hbf P3 Frankfurt (Main) Hbf P3 Vorfahrt II                         |          2941 |
| 100280 | Stuttgart-Bad Cannstatt P3 Bad Cannstatt P3 Parkhaus Wilhelmsplatz Ebenen -3 und -2 |          2487 |
| 100279 | Stuttgart-Bad Cannstatt P2 Bad Cannstatt P2 Parkhaus Wilhelmsplatz Ebenen -1 bis 6  |          2182 |
| 100090 | Freiburg (Breisgau) Hbf P1 Freiburg (Breisgau) Hbf P1 Tiefgarage am Bahnhof         |          1647 |
| 100291 | Ulm Hbf P2 Ulm Hbf P2 Parkplatz                                                     |          1519 |
| 100023 | Berlin Ostbahnhof P1 Berlin Ostbahnhof P1 Parkplatz                                 |          1362 |
| 100066 | Duisburg Hbf P2 Duisburg Hbf P2 Parkhaus UCI                                        |          1332 |

### elevator status
 
3705 objects, 10385 snapshots, 304421 changes

|       id | name                                                 |   num changes |
|---------:|:-----------------------------------------------------|--------------:|
| 10556568 | Tuttlingen ELEVATOR zum Gleis 4/5                    |          1196 |
| 10556569 | Tuttlingen ELEVATOR zu Gleis 1                       |          1194 |
| 10556567 | Tuttlingen ELEVATOR zum Gleis 2/3                    |          1192 |
| 10248843 | Regensburg Hbf ESCALATOR von Empfangshalle zu Brücke |           892 |
| 10417241 | Osnabrück Hbf ELEVATOR zu Gleis 4/5                  |           840 |
| 10354470 | Osnabrück Hbf ELEVATOR zu Gleis 1                    |           838 |
| 10460422 | Diepholz ELEVATOR zu Gleis 2/3                       |           838 |
| 10248859 | Regensburg Hbf ESCALATOR von Empfangshalle zu Brücke |           837 |
| 10417240 | Osnabrück Hbf ELEVATOR zu Gleis 2/3                  |           828 |
| 10466017 | Laupheim West ELEVATOR zu Gleis 2/3                  |           820 |

### stations
 
5402 objects, 627 snapshots, 50503 changes

|   id | name                         |   num changes |
|-----:|:-----------------------------|--------------:|
| 6714 | Westerland (Sylt)            |            20 |
| 1947 | Friedrichshafen Stadt        |            17 |
| 1859 | Frankfurt (Oder)             |            16 |
| 2514 | Hamburg Hbf                  |            16 |
| 3855 | Lüneburg                     |            16 |
| 4241 | München Ost                  |            16 |
| 4266 | München-Pasing               |            16 |
| 8192 | Flughafen BER - Terminal 1-2 |            16 |
| 1528 | Eisenach                     |            15 |
| 1634 | Erfurt Hbf                   |            15 |