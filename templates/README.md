# Deutsche Bahn API History

There was this [monumental talk](https://media.ccc.de/v/36c3-10652-bahnmining_-_punktlichkeit_ist_eine_zier)
in late 2019 about the *correctness* of the punctuality statistics published by
Deutsche Bahn, which got me interested in [api.deutschebahn.com](https://api.deutschebahn.com).

This repo contains non of the train schedule data. Instead it has change-logs of the
[parking api](https://developer.deutschebahn.com/store/apis/info?name=BahnPark&version=v1&provider=DBOpenData),
[station data api](https://developer.deutschebahn.com/store/apis/info?name=StaDa-Station_Data&version=v2&provider=DBOpenData)
and the [station facilities status api](https://developer.deutschebahn.com/store/apis/info?name=FaSta-Station_Facilities_Status&version=v2&provider=DBOpenData)
(status of elevators and escalators), **collected since late January 2020**.
 

## Summary

### free parking lots
 
%(summary_parking)s

### elevator status
 
%(summary_elevators)s

### stations
 
%(summary_stations)s


## Data

The APIs are sampled with separate cronjobs running these shell commands:

```shell script
# parking each 15 minutes
curl -X GET --header "Accept: application/json" \
    --header "Authorization: Bearer <YOUR_API_TOKEN>" \
    "https://api.deutschebahn.com/bahnpark/v1/spaces/occupancies" \
    > `date -Is -u`.json

# stations once a day
curl -X GET --header "Accept: application/json" \
    --header "Authorization: Bearer <YOUR_API_TOKEN>" \
    "https://api.deutschebahn.com/stada/v2/stations?searchstring=*" \
    > `date -Is -u`.json

# elevators each hour
curl -X GET --header "Accept: application/json" \
    --header "Authorization: Bearer <YOUR_API_TOKEN>" \
    "https://api.deutschebahn.com/fasta/v2/facilities?type=ESCALATOR,ELEVATOR"
    > `date -Is -u`.json
```
This simple setup does no error handling. If the endpoint is temporarily busy
the snapshot is lost.

Each API response is a list of objects which look like:

### parking

```json
{
  "allocation": {
    "validData": true,
    "capacity": 133,
    "category": 4,
    "text": "> 50"
  },
  "space": {
    "id": 100291,
    "label": "P2",
    "name": "Parkplatz Ulm Hauptbahnhof",
    "nameDisplay": "Ulm Hbf P2 Parkplatz",
    "station": {
      "id": 6323,
      "name": "Ulm Hbf"
    },
    "title": "Ulm Hbf P2 Ulm Hbf P2 Parkplatz"
  }
}
``` 

### stations

```json
{
  "aufgabentraeger": {
    "name": "Nahverkehrsservicegesellschaft Thüringen mbH",
    "shortName": "NVS"
  },
  "category": 6,
  "evaNumbers": [
    {
      "geographicCoordinates": {
        "coordinates": [11.593783, 50.93692],
        "type": "Point"
      },
      "isMain": true,
      "number": 8011058
    }
  ],
  "federalState": "Thüringen",
  "hasBicycleParking": true,
  "hasCarRental": false,
  "hasDBLounge": false,
  "hasLocalPublicTransport": true,
  "hasLockerSystem": false,
  "hasLostAndFound": false,
  "hasMobilityService": "no",
  "hasParking": false,
  "hasPublicFacilities": false,
  "hasRailwayMission": false,
  "hasSteplessAccess": "partial",
  "hasTaxiRank": false,
  "hasTravelCenter": false,
  "hasTravelNecessities": false,
  "hasWiFi": false,
  "mailingAddress": {
    "city": "Jena",
    "street": "Spitzweidenweg 28",
    "zipcode": "07743"
  },
  "name": "Jena Saalbf",
  "number": 3044,
  "priceCategory": 6,
  "regionalbereich": {
    "name": "RB Südost",
    "number": 2,
    "shortName": "RB SO"
  },
  "ril100Identifiers": [
    {
      "geographicCoordinates": {
        "coordinates": [11.593348001, 50.936519303],
        "type": "Point"
      },
      "hasSteamPermission": true,
      "isMain": true,
      "rilIdentifier": "UJS"
    }
  ],
  "stationManagement": {
    "name": "Chemnitz",
    "number": 115
  },
  "szentrale": {
    "name": "Erfurt Hbf",
    "number": 50,
    "publicPhoneNumber": "0361/3001055"
  },
  "timeTableOffice": {
    "email": "DBS.Fahrplan.Thueringen@deutschebahn.com",
    "name": "Bahnhofsmanagement Chemnitz"
  }
}
```

### elevators

```json
{
  "description": "zu Gleis 1",
  "equipmentnumber": 10354738,
  "geocoordX": 11.5873405,
  "geocoordY": 50.924981,
  "state": "ACTIVE",
  "stateExplanation": "available",
  "stationnumber": 3043,
  "type": "ELEVATOR"
}
```

## Change logs

The change-logs are collected in json files per year in [docs/data/](docs/data) 
using a self-baked format which does not contain too much space and allows committing 
new json lines with minimal diffs. 

All object keys are sorted alphabetically to avoid needless commit diffs.

To get access to all objects via python:
```python
from src.changelog_reader import ChangelogReader

for changelog_file, dates_file in ChangelogReader.get_changelog_files("stations"):
    reader = ChangelogReader(changelog_file, dates_file)
    for object_id in reader.object_ids():
        for timestamp, data in reader.iter_object(object_id):
            print(f"object {object_id} at time {timestamp} is {data}")
```

If an object was not listed during a snapshot, `data` will be `None`. 

The `reader.iter_object(object_id)` method iterates through all changes of the 
object. The `reader.iter_object_snapshots(object_id)` method iterates through 
each snapshot regardless if the object is changed or does not yet exist.


## Some graphics

Counting the number of elevators and escalators that do not have state
`ACTIVE` produces this interesting curve:

![plot of defect elevators per day](docs/img/elevators-per-day.png)

The different colors represent the amount of time that these machines where
inactive, 100%% meaning it was inactive the whole day.

The small repeating pikes align with the working days each week. This is
probably caused by a mixture of two things: Elevators might tend to break more often 
when used, and there are certainly more reports/complaints about defect machines
on workdays, compared to the weekends.
