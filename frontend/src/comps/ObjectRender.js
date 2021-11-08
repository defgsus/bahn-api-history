import React, { memo, useCallback, useState } from "react";


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


const Value = ({name, value, className}) => {
    if (typeof value !== "string")
        value = JSON.stringify(value);
    return (
        <div className={className}><b>{value}</b></div>
    );
};


const NestedRender = memo(({name, type, data, path, changed_paths}) => {
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

    const is_changed = changed_paths.filter(p => p.startsWith(path)).length > 0;

    let value_elem = null, render_value_changed = is_changed;
    switch (name) {
        case "geographicCoordinates":
            value_elem = `${data.type} ${data.coordinates[0]} ${data.coordinates[1]}`;
            break;

        case "aufgabentraeger":
            value_elem = `${data.name} (${data.shortName})`;
            break;

        case "mailingAddress":
            value_elem = Object.keys(data).sort().map(k => data[k]).join(" / ");
            break;

        case "stationManagement":
            value_elem = `${data.name} (${data.number})`;
            break;

        case "szentrale":
            value_elem = `${data.name} (${data.number}) (${data.publicPhoneNumber})`;
            break;

        case "regionalbereich":
            value_elem = `${data.name} (${data.number}) (${data.shortName})`;
            break;

        case "availability":
            if (data.monday) {
                value_elem = (
                    <table>
                        <tbody>
                        {["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "holiday"].map(day => {
                            const sub_path = path + "." + day;
                            const is_really_changed = is_changed && changed_paths.filter(p => p.startsWith(sub_path)).length > 0;
                            return (
                                <tr key={day} className={is_really_changed ? "changed" : ""}>
                                    <td>{day}&nbsp;</td>
                                    <td><b>{data[day].fromTime}</b></td>
                                    <td>-</td>
                                    <td><b>{data[day].toTime}</b></td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>
                );
                render_value_changed = false;
            }
            break;
    }

    if (value_elem) {
        return (
            <b className={render_value_changed ? "changed" : ""}>{value_elem}</b>
        )
    }

    return (
        <table>
            <tbody>
                {keys.map(key => {
                    const sub_path = path.length
                        ? path + "." + key
                        : key;
                    const is_really_changed = is_changed && changed_paths.filter(p => p.startsWith(sub_path)).length > 0;
                    return (
                        <tr key={key}>
                            <td className={is_really_changed ? "changed" : ""}>{key}:</td>
                            <td>{
                                typeof data[key] === "object"
                                    ? <NestedRender
                                        name={key}
                                        type={type}
                                        data={data[key]}
                                        path={sub_path}
                                        changed_paths={changed_paths}
                                    />
                                    : <Value name={key} value={data[key]} className={is_really_changed ? "changed" : ""}/>
                            }</td>
                        </tr>
                    );
                })}
            </tbody>
        </table>
    );
});


const ObjectRender = memo(({data, type, changes}) => {

    if (!data)
        return null;

    const changed_paths = [];
    if (changes) {
        for (const change_key of Object.keys(changes)) {
            for (const ch of changes[change_key]) {
                changed_paths.push(ch.path);
            }
        }
    }

    return (
        <div className={"object"}>
            <NestedRender type={type} data={data} path={""} changed_paths={changed_paths}/>
            {/*<pre>
                {JSON.stringify(data, null, 2)}
            </pre>*/}
        </div>
    );
});

export default ObjectRender;
