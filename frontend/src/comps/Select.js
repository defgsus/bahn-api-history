import React, { memo, useCallback, useContext } from "react";


const Select = ({options, value, onChange}) => {

    const updateValue = useCallback(
        e => {
            e.stopPropagation();
            e.preventDefault();
            onChange(e.target.value);
        },
        [onChange]
    );
    console.log("RENDER", value);
    return (
        <select value={value} onChange={updateValue}>
            {options.map(t => (
                <option key={t} value={t}>{t}</option>
            ))}
        </select>
    );
};

export default memo(Select);

