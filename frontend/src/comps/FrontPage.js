import React, { useCallback, useContext } from "react";
import state_context from "../context";
import Select from "./Select";
import ChangelogSelect from "./ChangelogSelect";
import Table from "./Table";


const FrontPage = (props) => {

    const {
        objects_table,
        dispatch,
    } = useContext(state_context);

    return (
        <div className={"front"}>

            <ChangelogSelect/>

            {objects_table && <Table
                {...objects_table}
            />}
        </div>
    );
};

export default FrontPage;

