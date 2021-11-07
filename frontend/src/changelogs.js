

export const get_objects_table = (state) => {
    const changelog =
        state.changelogs && state.changelogs[state.api_type]
            && state.changelogs[state.api_type][state.api_year];

    if (!changelog)
        return {columns: [], rows: []};

    const rows = [];
    for (const obj_id of Object.keys(changelog)) {
        const events = changelog[obj_id];
        const row = {
            id: obj_id,
            changes: events.length,
        };
        rows.push(row);
        if (rows.length > 30)
            break;
    }

    return {
        columns: ["id", "changes"],
        rows: rows,
    }
};