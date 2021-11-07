import React, { useContext } from "react";
import state_context from "../context";


const FrontPage = (props) => {

    const {
        api_type, api_types,
        api_year, api_years,
        dispatcher
    } = useContext(state_context);

    return (
        <div className={"front"}>

            <select value={api_type} onChange={
                e => dispatcher({type: "SET_API", payload: {type: e.target.value, year: api_year}})
            }>
                {api_types.map(t => (
                    <option key={t} value={t}>{t}</option>
                ))}
            </select>

            <select value={api_year} onChange={
                e => dispatcher({type: "SET_API", payload: {type: api_type, year: e.target.value}})
            }>
                {api_years.map(t => (
                    <option key={t} value={t}>{t}</option>
                ))}
            </select>

        </div>
    );
};

export default FrontPage;

