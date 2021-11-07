import {useCallback, useReducer} from "react";
import PropTypes from 'prop-types';

import state_context from "./context";
import {get_objects_table} from "./changelogs";


const DEFAULT_STATE = {
    api_types: ["stations", "elevators", "parking"],
    api_years: ["2020", "2021"],
    api_type: "stations",
    api_year: "2020",
    changelogs: null,
    objects_table: null,
};



export function reducer(state, action) {
    console.log("ACTION", action);

    switch (action.type) {

        case "SET_API":

            //if (!state.changelogs || state.changelogs[action.payload.type]
            //        || !state.changelogs[action.payload.type][action.payload.year])
                //load_data(action.payload.type, action.payload.year);

            state = {
                ...state,
                api_type: action.payload.type,
                api_year: action.payload.year,
            };
            state.objects_table = get_objects_table(state);
            return state;

        case "LOAD_CHANGELOG_SUCCESS":
            state = {
                ...state,
                changelogs: {
                    ...state.changelogs,
                    [state.api_type]: {
                        ...(state.changelogs && state.changelogs[state.api_type]),
                        [state.api_year]: action.data,
                    }
                },
            };
            state.objects_table = get_objects_table(state);
            return state;

        default:
            return state;
    }
}


const StateProvider = ({children}) => {
    const [state, dispatch] = useReducer(reducer, DEFAULT_STATE);

    const request = useCallback(
        (action_name, method, url) => {
            const req = new XMLHttpRequest();
            req.open(method, url);
            req.onload = e => {
                const data = JSON.parse(req.response);
                dispatch({type: `${action_name}_SUCCESS`, event: e, data});
            };
            req.onerror = e => {
                dispatch({type: `${action_name}_FAILED`, event: e});
            };
            dispatch({type: `${action_name}_STARTED`, method, url});
            req.send();
        },
        [dispatch]
    );

    return (
        <state_context.Provider value={{...state, request, dispatch}}>
            {children}
        </state_context.Provider>
    );
};

StateProvider.propTypes = {
    children: PropTypes.element.isRequired,
};

export default StateProvider;