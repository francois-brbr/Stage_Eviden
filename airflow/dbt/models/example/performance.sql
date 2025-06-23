-- models/performance.sql

WITH first_values AS (
    SELECT
        FIRST_VALUE(nasdaq) OVER (ORDER BY date) AS first_nasdaq,
        FIRST_VALUE(dji) OVER (ORDER BY date) AS first_dji,
        FIRST_VALUE(fchi) OVER (ORDER BY date) AS first_fchi,
        FIRST_VALUE(gspc) OVER (ORDER BY date) AS first_gspc,
        FIRST_VALUE(n225) OVER (ORDER BY date) AS first_n225,
        FIRST_VALUE(stoxx50e) OVER (ORDER BY date) AS first_stoxx50e
    FROM public.stock_data
    WHERE nasdaq IS NOT NULL AND dji IS NOT NULL AND fchi IS NOT NULL AND gspc IS NOT NULL AND n225 IS NOT NULL AND stoxx50e IS NOT NULL
    LIMIT 1
),

last_values AS (
    SELECT
        LAST_VALUE(nasdaq) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_nasdaq,
        LAST_VALUE(dji) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_dji,
        LAST_VALUE(fchi) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_fchi,
        LAST_VALUE(gspc) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_gspc,
        LAST_VALUE(n225) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_n225,
        LAST_VALUE(stoxx50e) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_stoxx50e
    FROM public.stock_data
    LIMIT 1
)

SELECT
    'NASDAQ' AS indice,
    ROUND(((last_nasdaq - first_nasdaq) / NULLIF(first_nasdaq, 0) * 100)::numeric, 2) AS performance,
    first_nasdaq AS first_value,
    last_nasdaq AS last_value
FROM first_values, last_values

UNION ALL

SELECT
    'DOW JONHS INDUSTRIAL' AS indice,
    ROUND(((last_dji - first_dji) / NULLIF(first_dji, 0) * 100)::numeric, 2) AS performance,
    first_dji AS first_value,
    last_dji AS last_value
FROM first_values, last_values

UNION ALL

SELECT
    'CAC40' AS indice,
    ROUND(((last_fchi - first_fchi) / NULLIF(first_fchi, 0) * 100)::numeric, 2) AS performance,
    first_fchi AS first_value,
    last_fchi AS last_value
FROM first_values, last_values

UNION ALL

SELECT
    'S&P500' AS indice,
    ROUND(((last_gspc - first_gspc) / NULLIF(first_gspc, 0) * 100)::numeric, 2) AS performance,
    first_gspc AS first_value,
    last_gspc AS last_value
FROM first_values, last_values

UNION ALL

SELECT
    'NIKKEI225' AS indice,
    ROUND(((last_n225 - first_n225) / NULLIF(first_n225, 0) * 100)::numeric, 2) AS performance,
    first_n225 AS first_value,
    last_n225 AS last_value
FROM first_values, last_values

UNION ALL

SELECT
    'EURO STOXX50E' AS indice,
    ROUND((last_stoxx50e - first_stoxx50e) / NULLIF(first_stoxx50e, 0) * 100) AS performance,
    first_stoxx50e AS first_value,
    last_stoxx50e AS last_value
FROM first_values, last_values