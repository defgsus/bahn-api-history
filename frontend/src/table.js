

export const paginate_table = (table) => {
    const rows = table.full_rows;

    if (typeof table.per_page === "undefined")
        table.per_page = 23;

    table.pages = Math.floor(rows.length / table.per_page);

    if (typeof table.page === "undefined")
        table.page = 0;
    else
        table.page = Math.min(table.page, table.pages);

    if (typeof table.sort_by === "undefined")
        table.sort_by = null;
    if (typeof table.sort_asc === "undefined")
        table.sort_asc = false;

    table.row_start = table.page * table.per_page;
    table.row_end = Math.min(rows.length, (table.page + 1) * table.per_page);

    if (table.sort_by) {
        table.full_rows.sort((a, b) => row_compare(table, a, b))
    }

    table.rows = rows.slice(table.row_start, table.row_end);
};


const row_compare = (table, r1, r2) => {
    const
        key = table.sort_by,
        v1 = r1[key],
        v2 = r2[key];

    let result = v1 < v2;

    result = result ? -1 : 1;
    if (!table.sort_asc)
        result = -result;

    return result;
};
