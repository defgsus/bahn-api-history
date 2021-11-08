import React, { memo, useCallback, useState } from "react";
import ObjectRender from "./ObjectRender";

const ChangesRender = memo(({changes}) => {
    if (!changes)
        return null;

    const elems = [];
    let i = 0;
    for (const change_key of Object.keys(changes)) {
        for (const change of changes[change_key]) {
            const path = change.path;
            elems.push(
                <li
                    key={++i}
                    className={change_key === "add" ? "green" : change_key === "remove" ? "red" : ""}
                >
                    {change_key} {path}
                </li>
            );
        }
    }
    return (
        <ul>
            {elems}
        </ul>
    );
});

const Snapshots = ({object_snapshots, type}) => {

    if (!object_snapshots || !object_snapshots.length)
        return null;

    let [index, set_index] = useState(0);
    let [as_json, set_as_json] = useState(0);

    index = Math.min(index, object_snapshots.length - 1);

    return (
        <div>
            <hr/>
            <div className={"snapshots grid-x"}>
                <div className={"timestamps"}>
                    {object_snapshots.map((s, i) => (
                        <div
                            key={s.dt}
                            className={"timestamp clickable" + (i === index ? " selected" : "")}
                            onClick={e => set_index(i)}
                        >
                            {s.dt.replace('T', ' ')}
                        </div>
                    ))}
                </div>

                <div className={"snapshot grow"}>
                    <div className={"grid-x"}>
                        <div className={"grow"}>
                            <ChangesRender changes={object_snapshots[index].changes}/>
                        </div>
                        <div>
                            {as_json
                                ? <button onClick={e => set_as_json(0)}>text</button>
                                : <button onClick={e => set_as_json(1)}>json</button>
                            }
                        </div>
                    </div>

                    {as_json
                        ? <pre>
                            {JSON.stringify(object_snapshots[index].object, null, 2)}
                        </pre>
                        : <ObjectRender data={object_snapshots[index].object} type={type}/>
                    }
                </div>
            </div>
        </div>
    );
};

export default memo(Snapshots);

