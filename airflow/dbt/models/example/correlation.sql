-- models/correlation.sql

WITH nasdaq_gspc_correlation AS (
    SELECT
        'NASDAQ' AS indice_a,
        'S&P500' AS indice_b,
        ROUND(CORR(nasdaq, gspc)::numeric, 2) AS correlation
    FROM
        public.stock_data_prices
),

nasdaq_dji_correlation AS (
    SELECT
        'NASDAQ' AS indice_a,
        'DOW JOHNS INDUSTRIAL' AS indice_b,
        ROUND(CORR(nasdaq, dji)::numeric, 2) AS correlation
    FROM
        public.stock_data_prices
),

gspc_dji_correlation AS (
    SELECT
        'S&P500' AS indice_a,
        'DOW JOHNS INDUSTRIAL' AS indice_b,
        ROUND(CORR(gspc, dji)::numeric, 2) AS correlation
    FROM
        public.stock_data_prices
),


cac40_stoxx50_correlation AS (
    SELECT
        'CAC40' AS indice_a,
        'EURO STOXX50E' AS indice_b,
        ROUND(CORR(fchi, stoxx50e)::numeric, 2) AS correlation
    FROM
        public.stock_data_prices
),

cac40_nikkei_correlation AS (
    SELECT
        'CAC40' AS indice_a,
        'NIKKEI225' AS indice_b,
        ROUND(CORR(fchi, n225)::numeric, 2) AS correlation
    FROM
        public.stock_data_prices
)

SELECT * FROM nasdaq_gspc_correlation
UNION ALL
SELECT * FROM nasdaq_dji_correlation
UNION ALL
SELECT * FROM gspc_dji_correlation
UNION ALL
SELECT * FROM cac40_stoxx50_correlation
UNION ALL
SELECT * FROM cac40_nikkei_correlation