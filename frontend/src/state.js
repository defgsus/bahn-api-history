import {useCallback, useReducer} from "react";
import PropTypes from 'prop-types';

import state_context from "./context";
import {get_objects_table, render_object_snapshots} from "./changelogs";
import {paginate_table} from "./table";


const DEFAULT_STATE = {
    error: null,
    api_types: ["stations", "elevators", "parking"],
    api_years: ["2020", "2021"],
    api_type: "stations",
    api_year: "2020",
    changelogs: null,
    table_loading: false,
    objects_table: null,
    object_snapshots: null,
};



export function reducer(state, action) {
    console.log("ACTION", action);
    console.log("OLD STATE", state);

    switch (action.type) {

        case "SET_API":
            state = {
                ...state,
                api_type: action.payload.type,
                api_year: action.payload.year,
                object_snapshots: null,
            };
            state.objects_table = {
                ...state.objects_table,
                ...get_objects_table(state),
            };
            paginate_table(state.objects_table);
            return state;

        case "LOAD_CHANGELOG_STARTED":
            return {
                ...state,
                table_loading: true,
            };

        case "LOAD_CHANGELOG_FAILED":
            return {
                ...state,
                table_loading: false,
                error: "Failed loading data",
            };

        case "LOAD_CHANGELOG_SUCCESS":
            state = {
                ...state,
                table_loading: false,
                changelogs: {
                    ...state.changelogs,
                    [state.api_type]: {
                        ...(state.changelogs && state.changelogs[state.api_type]),
                        [state.api_year]: action.data,
                    }
                },
            };
            state.objects_table = {
                ...state.objects_table,
                ...get_objects_table(state),
            };
            paginate_table(state.objects_table);
            return state;

        case "SET_TABLE_PARAMS":
            state = {
                ...state,
                objects_table: {
                    ...state.objects_table,
                    ...action.payload,
                }
            };
            paginate_table(state.objects_table);
            return state;

        case "RENDER_OBJECT":
            return {
                ...state,
                object_snapshots: render_object_snapshots(
                    action.id,
                    state.changelogs[state.api_type][state.api_year],
                ),
            };

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
