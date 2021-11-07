import React, { useCallback } from "react";


const TableHead = ({columns}) => {
    return (
        <thead>
            <tr>
                {columns.map((c, i) => (
                    <th key={i}>{c}</th>
                ))}
            </tr>
        </thead>
    );
};


const TableBody = ({columns, rows}) => {
    return (
        <tbody>
            {rows.map((row, y) => (
                <tr key={y}>
                    {columns.map((c, x) => (
                        <td key={x}>
                            {row[c] || "-"}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>

    );
};



const Table = ({columns, rows}) => {

    const updateValue = useCallback(
        e => {
            e.stopPropagation();
            e.preventDefault();
            onChange(e.target.value);
        },
        []
    );

    return (
        <table>
            <TableHead columns={columns}/>
            <TableBody columns={columns} rows={rows}/>
        </table>
    );
};

export default Table;

