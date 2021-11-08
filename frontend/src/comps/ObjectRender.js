import React, { memo, useCallback, useState } from "react";


const Value = ({name, value}) => {
    if (typeof value !== "string")
        value = JSON.stringify(value);
    return (
        <div className={"value"}><b>{value}</b></div>
    );
};


const NestedRenderX = memo(({data}) => {
    const keys = Object.keys(data).sort();
    const simple_keys = keys.filter(k => typeof data[k] !== "object");

    return (
        <div className={"grid-x nowrap"}>
            <div className={"keys"}>
                {keys.map(key => (
                    <div key={key}>{key}:</div>
                ))}
            </div>
            <div className={"values"}>
                {keys.map(key => (
                    typeof data[key] === "xxobject"
                        ? <NestedRender key={key} name={key} type={type} data={data[key]}/>
                        : <Value key={key} name={key} value={data[key]}/>
                ))}
            </div>
        </div>
    );
});

const SORT_KEYS = {
    "stations": [
        "number",
        "name",
        "mailingAddress",
        "federalState",
        "aufgabentraeger",
        "stationManagement",
        "szentrale",
        "regionalbereich",
        "timeTableOffice",
        "evaNumbers",
        "ril100Identifiers",
        "category",
        "priceCategory",
    ],
    "elevators": [],
    "parking": [
        "space",
        "allocation",
    ],
};


const NestedRender = memo(({name, type, data}) => {
    const keys = Object.keys(data).sort(
        (a, b) => {
            const
                ia = SORT_KEYS[type].indexOf(a),
                ib = SORT_KEYS[type].indexOf(b);
            if (ia >= 0) {
                if (ib >= 0)
                    return ia < ib ? -1 : 1;
                return -1;
            }
            if (ib >= 0) {
                return 1;
            }
            return a < b ? -1 : 1;
        }
    );
    //const simple_keys = keys.filter(k => typeof data[k] !== "object");

    switch (name) {
        case "geographicCoordinates":
            return <b>{`${data.type} ${data.coordinates[0]} ${data.coordinates[1]}`}</b>;

        case "aufgabentraeger":
            return <b>{`${data.name} (${data.shortName})`}</b>;

        case "mailingAddress":
            return <b>{
                Object.keys(data).sort().map(k => data[k]).join(" / ")
            }</b>;

        case "stationManagement":
            return <b>{`${data.name} (${data.number})`}</b>;

        case "szentrale":
            return <b>{`${data.name} (${data.number}) (${data.publicPhoneNumber})`}</b>;

        case "regionalbereich":
            return <b>{`${data.name} (${data.number}) (${data.shortName})`}</b>;

        case "availability":
            if (data.monday) {
                return (
                    <table>
                        <tbody>
                            {["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "holiday"].map(day => (
                                <tr>
                                    <td>{day}&nbsp;</td>
                                    <td><b>{data[day].fromTime}</b></td>
                                    <td>-</td>
                                    <td><b>{data[day].toTime}</b></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )
            }
    }

    return (
        <table>
            <tbody>
                {keys.map(key => (
                    <tr key={key}>
                        <td>{key}:</td>
                        <td>{
                            typeof data[key] === "object"
                                ? <NestedRender key={key} name={key} type={type} data={data[key]}/>
                                : <Value key={key} name={key} value={data[key]}/>
                        }</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
});


const ObjectRender = memo(({data, type}) => {

    if (!data)
        return null;

    return (
        <div className={"object"}>
            <NestedRender type={type} data={data}/>
            {/*<pre>
                {JSON.stringify(data, null, 2)}
            </pre>*/}
        </div>
    );
});

export default ObjectRender;
