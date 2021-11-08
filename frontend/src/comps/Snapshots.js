import React, {memo, useCallback, useEffect, useState} from "react";
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

const ObjectSnapshot = memo(({snapshot, type, as_json, set_as_json}) => {
    return (
        <div>
            <div className={"grid-x"}>
                <div className={"grow"}/>
                <div>
                    {as_json
                        ? <button onClick={e => set_as_json(0)}>text</button>
                        : <button onClick={e => set_as_json(1)}>json</button>
                    }
                </div>
            </div>

            {as_json
                ? <pre>{JSON.stringify(snapshot.object, null, 2)}</pre>
                : <ObjectRender data={snapshot.object} type={type} changes={snapshot.changes}/>
            }

            <hr/>
            <div className={"grid-x"}>
                <div className={"grow"}>
                    <ChangesRender changes={snapshot.changes}/>
                </div>
            </div>

        </div>
    );
});


const AllChanges = memo(({snapshots, type}) => {
    return (
        <div>
            <ul>
                {snapshots.map(sn => (
                    <li key={sn.dt}>
                        {sn.dt}
                        <ChangesRender changes={sn.changes}/>
                    </li>
                ))}
            </ul>
        </div>
    );
});


const Snapshots = memo(({object_snapshots, type}) => {

    if (!object_snapshots || !object_snapshots.length)
        return null;

    let [index, set_index] = useState(-1);
    let [as_json, set_as_json] = useState(0);

    index = Math.max(-1, Math.min(index, object_snapshots.length - 1));

    useEffect(() => {
        const handler = e => {
            let handled = false;
            switch (e.key) {
                case "ArrowUp": if (index > -1) { set_index(index - 1); handled = true; } break;
                case "ArrowDown":
                    if (index < object_snapshots.length-1) { set_index(index + 1); handled = true; }
                    break;
            }
            if (handled) {
                e.stopPropagation();
                e.preventDefault();
            }
        };
        window.addEventListener("keydown", handler);

        return () => window.removeEventListener("keydown", handler);
    }, [index, set_index, object_snapshots]);

    return (
        <div>
            <hr/>
            <div className={"snapshots grid-x"}>
                <div className={"timestamps"}>
                    <div
                        className={"timestamp clickable" + (-1 === index ? " selected" : "")}
                        onClick={e => set_index(-1)}
                    >
                        all
                    </div>
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
                    {index >= 0
                        ? <ObjectSnapshot
                            snapshot={object_snapshots[index]} type={type}
                            as_json={as_json} set_as_json={set_as_json}
                        />
                        : <AllChanges snapshots={object_snapshots} type={type}/>
                    }
                </div>
            </div>
        </div>
    );
});

export default Snapshots;

