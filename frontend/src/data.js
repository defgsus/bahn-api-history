import {useContext} from "react";
import state_context from "./context";

export function load_data(api_type, year) {

    //const { dispatcher } = useContext(state_context);

    const req = new XMLHttpRequest();
    req.open("GET", `data/${api_type}/${year}-changelog.json`);
    //req.open("GET", "style.css");
    //req.onload = e => dispatcher({type: "LOAD_API_DATA_SUCCESS", payload: e});
    req.onload = e => console.log("RESP", e);
    //dispatcher({type: "LOAD_API_DATA_STARTED"});
    req.send();
}