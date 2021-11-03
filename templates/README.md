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
 
%(summary_parking)s

### elevator status
 
%(summary_elevators)s

### stations
 
%(summary_stations)s