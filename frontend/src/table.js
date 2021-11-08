

export const paginate_table = (table) => {
    let rows = table.full_rows;
    table.total_count = rows.length;

    if (typeof table.per_page === "undefined")
        table.per_page = 10;

    table.pages = Math.floor(rows.length / table.per_page);

    if (typeof table.page === "undefined")
        table.page = 0;
    else
        table.page = Math.min(table.page, table.pages);

    if (typeof table.sort_by === "undefined")
        table.sort_by = "id";
    if (typeof table.sort_asc === "undefined")
        table.sort_asc = true;

    if (typeof table.filter === "undefined")
        table.filter = "";

    table.row_start = table.page * table.per_page;
    table.row_end = Math.min(rows.length, (table.page + 1) * table.per_page);

    if (table.filter?.length) {
        const filter_n = parseInt(table.filter);
        rows = rows.filter(row => {
            for (const k of Object.keys(row)) {
                if (k === "first_date")
                    continue;

                const v = row[k];
                if (typeof v === "string")
                    if (v.toLowerCase().indexOf(table.filter) >= 0)
                        return true;
                if (typeof v === "number")
                    if (v === filter_n)
                        return true;
            }
        })
    }

    if (table.sort_by) {
        table.full_rows.sort((a, b) => row_compare(table, a, b))
    }

    table.row_count = rows.length;

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
