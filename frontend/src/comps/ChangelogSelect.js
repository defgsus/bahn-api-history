import React, { memo, useCallback, useContext } from "react";
import state_context from "../context";
import Select from "./Select";


const ChangelogSelect = () => {

    const {
        api_type, api_types,
        api_year, api_years,
        changelogs,
        dispatch, request,
    } = useContext(state_context);

    const updateApiType = useCallback(
        v => {
            dispatch({type: "SET_API", payload: {type: v, year: api_year}});
            if (!changelogs || !changelogs[v] || !changelogs[v][api_year])
                request("LOAD_CHANGELOG", "GET", `data/${v}/${api_year}-changelog.json`)
        },
        [api_year, dispatch]
    );

    const updateApiYear = useCallback(
        v => {
            dispatch({type: "SET_API", payload: {type: api_type, year: v}});
            if (!changelogs || !changelogs[api_type] || !changelogs[api_type][v])
                request("LOAD_CHANGELOG", "GET", `data/${api_type}/${v}-changelog.json`)
        },
        [api_type, dispatch]
    );

    return (
        <div>

            <Select
                options={api_types}
                value={api_type}
                onChange={updateApiType}
            />

            <Select
                options={api_years}
                value={api_year}
                onChange={updateApiYear}
            />

        </div>
    );
};

export default memo(ChangelogSelect);

