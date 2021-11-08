import React, { useCallback, useContext } from "react";
import state_context from "../context";
import Select from "./Select";
import ChangelogSelect from "./ChangelogSelect";
import Table from "./Table";


const FrontPage = () => {

    const {
        error,
        objects_table, table_loading,
        dispatch,
    } = useContext(state_context);

    const set_table_page = useCallback(v => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {page: v}})
    }, []);

    const set_table_per_page = useCallback(v => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {per_page: v}})
    }, []);

    const set_table_sort = useCallback((c, a) => {
        dispatch({type: "SET_TABLE_PARAMS", payload: {sort_by: c, sort_asc: a}})
    }, []);

    return (
        <div className={"front"}>

            <ChangelogSelect/>

            {error ? <div className={"error"}>{error}</div> : null}

            {table_loading
                ? "loading..."
                : objects_table
                    ? <Table
                        {...objects_table}
                        set_page={set_table_page}
                        set_per_page={set_table_per_page}
                        set_sort={set_table_sort}
                    />
                    :  null
            }
        </div>
    );
};

export default FrontPage;

