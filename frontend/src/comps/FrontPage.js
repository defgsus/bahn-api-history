import React, { useCallback, useContext, useEffect } from "react";
import state_context from "../context";
import Select from "./Select";
import ChangelogSelect from "./ChangelogSelect";
import Table from "./Table";
import Snapshots from "./Snapshots";


const FrontPage = () => {

    const {
        error,
        objects_table, table_loading, table_loading_progress,
        object_snapshots,
        api_type, api_year, changelogs, request,
        dispatch,
    } = useContext(state_context);

    // load data on startup
    useEffect(() => {
        if (!changelogs || !changelogs[api_type] || !changelogs[api_type][api_year])
            request("LOAD_CHANGELOG", "GET", `data/${api_type}/${api_year}-changelog.json`)
    }, []);

    const set_table_page = useCallback(v => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {page: v}})
    }, []);

    const set_table_per_page = useCallback(v => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {per_page: v}})
    }, []);

    const set_table_sort = useCallback((c, a) => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {sort_by: c, sort_asc: a}})
    }, []);

    const set_table_filter = useCallback(v => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {filter: v}})
    }, []);

    const table_row_click = useCallback((row, y) => {
        dispatch({type: "RENDER_OBJECT", id: row.id})
    }, []);

    return (
        <div className={"front"}>

            <ChangelogSelect/>

            {error ? <div className={"error"}>{error}</div> : null}

            {table_loading
                ? <div>loading... {table_loading_progress}%</div>
                : objects_table
                    ? <Table
                        {...objects_table}
                        set_page={set_table_page}
                        set_per_page={set_table_per_page}
                        set_sort={set_table_sort}
                        set_filter={set_table_filter}
                        row_click={table_row_click}
                    />
                    :  null
            }

            <Snapshots object_snapshots={object_snapshots} type={api_type}/>
        </div>
    );
};

export default FrontPage;

