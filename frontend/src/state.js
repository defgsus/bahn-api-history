import { useReducer } from "react";
import state_context from "./context";
import {load_data} from "./data";


const DEFAULT_STATE = {
    api_types: ["stations", "elevators", "parking"],
    api_years: ["2020", "2021"],
    api_type: "stations",
    api_year: "2020",
    changelogs: null,
};



export function reducer(state, action) {
    console.log("ACTION", action);

    switch (action.type) {

        case "SET_API":

            if (!state.changelogs || state.changelogs[action.payload.type]
                    || !state.changelogs[action.payload.type][action.payload.year])
                load_data(action.payload.type, action.payload.year);

            return {
                ...state,
                api_type: action.payload.type,
                api_year: action.payload.year,
            };

        default:
            return state;
    }
}


export const StateProvider = ({children}) => {
    const [state, dispatcher] = useReducer(reducer, DEFAULT_STATE);

    return (
        <state_context.Provider value={{...state, dispatcher}}>
            {children}
        </state_context.Provider>
    );
};
