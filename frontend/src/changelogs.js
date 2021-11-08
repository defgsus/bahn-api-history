import { Map, List, fromJS } from "immutable"

window.fromJS = fromJS;

export const get_objects_table = (state) => {
    const changelog =
        state.changelogs && state.changelogs[state.api_type]
            && state.changelogs[state.api_type][state.api_year];

    if (!changelog)
        return {columns: [], full_rows: []};

    const rows = [];
    for (const obj_id of Object.keys(changelog)) {
        const events = changelog[obj_id];
        const row = {
            id: obj_id,
            changes: events.length,
        };
        add_object_to_row(row, events, state.api_type);
        rows.push(row);
    }

    return {
        columns: [
            {name: "id"},
            {name: "changes", align: "right"},
            {name: "name"},
            {name: "first_date"},
        ],
        full_rows: rows,
    }
};


const add_object_to_row = (row, events, type) => {
    for (const snapshot of object_generator(events)) {
        const o = snapshot.object;
        if (o && !row.first_date)
            row.first_date = snapshot.dt;
        switch (type) {
            case "stations":
                if (o?.name)
                    row.name = o.name;
                if (row.name)
                    return;
                break;

            case "elevators":
                if (o?.name)
                    row.name = o.name;
                if (row.name)
                    return;
                break;

            case "parking":
                if (o?.space?.nameDisplay)
                    row.name = o.space.nameDisplay;
                if (row.name)
                    return;
                break;
        }
    }
};


export function render_object_snapshots(obj_id, changelogs) {
    const snapshots = [];
    for (const snapshot of object_generator(changelogs[obj_id]))
        snapshots.push(snapshot);
    return snapshots;
}


export function* object_generator(events) {
    let cur_object = null;
    for (const cl of events) {
        const dt = cl.date;

        if (cl.init) {
            cur_object = fromJS(cl.init);
        }

        if (cl.changes) {
            for (const change_key of Object.keys(cl.changes)) {
                for (const change of cl.changes[change_key]) {
                    const path = change.path.split(".");

                    if (!cur_object)
                        throw `'${change_key}' ${change.path} before 'init' @ ${dt}`;

                    switch (change_key) {
                        case "add":
                            cur_object = cur_object.updateIn(
                                path, old_value => {
                                   return change.value;
                                }
                            );
                            break;

                        case "remove":
                            cur_object = cur_object.removeIn(path);
                            break;

                        case "replace":
                            cur_object = cur_object.updateIn(
                                path, old_value => change.value
                            )
                    }
                }
            }
        }

        yield {
            dt: dt.replace("T", " "),
            object: cur_object && cur_object.toJS(),
            changes: cl.changes,
        };
    }
}