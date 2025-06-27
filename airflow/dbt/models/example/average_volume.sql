-- models/average_volume.sql

SELECT
    'NASDAQ' AS indice,
    ROUND(AVG(nasdaq)::numeric,2) AS average_volume
FROM public.stock_data_volumes
WHERE nasdaq IS NOT NULL

UNION ALL

SELECT
    'DOW JONHS INDUSTRIAL' AS indice,
    ROUND(AVG(dji)::numeric,2) AS average_volume
FROM public.stock_data_volumes
WHERE dji IS NOT NULL

UNION ALL

SELECT
    'CAC40' AS indice,
    ROUND(AVG(fchi)::numeric,2) AS average_volume
FROM public.stock_data_volumes
WHERE fchi IS NOT NULL

UNION ALL

SELECT
    'S&P500' AS indice,
    ROUND(AVG(gspc)::numeric,2) AS average_volume
FROM public.stock_data_volumes
WHERE gspc IS NOT NULL

UNION ALL

SELECT
    'NIKKEI225' AS indice,
    ROUND(AVG(n225)::numeric,2) AS average_volume
FROM public.stock_data_volumes
WHERE n225 IS NOT NULL

UNION ALL

SELECT
    'EURO STOXX50E' AS indice,
    ROUND(AVG(stoxx50e)::numeric,2) AS average_volume
FROM public.stock_data_volumes
WHERE stoxx50e IS NOT NULL