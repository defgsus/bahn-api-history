import React, { useCallback, memo } from "react";
import Number from "./Number";

//const sort_icons = ["▵", "▴", "▿", "▾"];
const sort_icons = ["△", "▲", "▽", "▼"];

const TableHead = memo(({columns, sort_by, sort_click, sort_asc}) => {
    return (
        <thead>
            <tr>
                {columns.map((c, i) => (
                    <th key={i}>
                        <div
                            className={"grid-x clickable"}
                            onClick={e => sort_click(c.name)}
                        >
                            <div className={"title grow"}>{c.name}</div>
                            <div
                                className={"sort" + (sort_by === c.name ? " active" : "")}
                            >{
                                sort_asc
                                    ? sort_by === c.name
                                        ? sort_icons[1] : sort_icons[0]
                                    : sort_by === c.name
                                        ? sort_icons[3] : sort_icons[2]
                            }</div>
                        </div>
                    </th>
                ))}
            </tr>
        </thead>
    );
});


const TableBody = memo(({columns, rows, row_click}) => {

    return (
        <tbody>
            {rows.map((row, y) => (
                <tr
                    key={y}
                    onClick={e => { if (row_click) row_click(row, y); }}
                    className={"" + (row_click ? " clickable" : "")}
                >
                    {columns.map((c, x) => (
                        <td key={x} className={"" + (c.align ? c.align : "")}>
                            {row[c.name] || "-"}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>

    );
});


const TablePager = memo(({total_count, page, set_page, pages, per_page, set_per_page}) => {
    return (
        <div className={"pager grid-x margin-right"}>
            <div className={"grow"}/>
            <div>total: {total_count}</div>
            <div>
                page&nbsp;
                <Number min={1} max={10000} value={page} set_value={set_page} offset={1}/>
                &nbsp;/ {pages + 1}
            </div>
            <div>
                <Number min={1} max={10000} value={per_page} set_value={set_per_page}/>
                &nbsp;per page
            </div>
        </div>
    );
});



const Table = ({
    columns, rows, full_rows,
    page, set_page, pages,
    per_page, set_per_page,
    sort_by, sort_asc,
    set_sort,
    row_click,
}) => {

    const sort_click = useCallback(c => {
        if (sort_by !== c)
            set_sort(c, sort_asc);
        else
            set_sort(c, !sort_asc);
    }, [sort_by, sort_asc]);

    return (
        <div className={"table"}>
            <TablePager
                total_count={full_rows.length}
                page={page} set_page={set_page}
                pages={pages}
                per_page={per_page}
                set_per_page={set_per_page}
            />
            <table>
                <TableHead
                    columns={columns}
                    sort_by={sort_by}
                    sort_asc={sort_asc}
                    sort_click={sort_click}
                />
                <TableBody
                    columns={columns}
                    rows={rows}
                    row_click={row_click}
                />
            </table>
        </div>
    );
};

export default memo(Table);

