import React, { memo, useCallback } from "react";


const Select = memo(({options, value, onChange}) => {

    const updateValue = useCallback(
        e => {
            e.stopPropagation();
            e.preventDefault();
            onChange(e.target.value);
        },
        [onChange]
    );

    return (
        <select value={value} onChange={updateValue}>
            {options.map(t => (
                <option key={t} value={t}>{t}</option>
            ))}
        </select>
    );
});

export default Select;

