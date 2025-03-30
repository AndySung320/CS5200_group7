SELECT
    employee_id,
    product_id,
    sales
FROM
    sales AS s
WHERE
    product_id = (
        SELECT product_id
        FROM sales
        WHERE employee_id = s.employee_id
        AND sales = (
            SELECT MAX(sales)
            FROM sales
            WHERE employee_id = s.employee_id
        )
        ORDER BY product_id ASC
        LIMIT 1
    )
ORDER BY
    employee_id ASC;