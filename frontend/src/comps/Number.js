import React, { memo, useCallback } from "react";


const Number = ({value, set_value, min, max, step, offset}) => {

    const onChange = useCallback(
        e => {
            e.stopPropagation();
            e.preventDefault();
            let value = e.target.value;
            if (typeof offset === "number")
                value -= offset;
            set_value(value);
        },
        [set_value, offset]
    );

    let display_value = value;
    if (typeof offset === "number")
        display_value = display_value + offset;

    return (
        <input
            className={"number"}
            type={"number"}
            value={display_value}
            min={min}
            max={max}
            step={step}
            onChange={onChange}
        />
    );
};

export default memo(Number);

