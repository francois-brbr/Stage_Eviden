-- models/combined_correlations.sql

WITH nasdaq_gspc_correlation AS (
    SELECT
        'NASDAQ' AS index_a,
        'S&P500' AS index_b,
        ROUND(CORR(nasdaq, gspc)::numeric, 2) AS correlation
    FROM
        public.stock_data
),

nasdaq_dji_correlation AS (
    SELECT
        'NASDAQ' AS index_a,
        'DOW JOHNS INDUSTRIAL' AS index_b,
        ROUND(CORR(nasdaq, dji)::numeric, 2) AS correlation
    FROM
        public.stock_data
),

gspc_dji_correlation AS (
    SELECT
        'S&P500' AS index_a,
        'DOW JOHNS INDUSTRIAL' AS index_b,
        ROUND(CORR(gspc, dji)::numeric, 2) AS correlation
    FROM
        public.stock_data
),


cac40_stoxx50_correlation AS (
    SELECT
        'CAC40' AS index_a,
        'EURO STOXX50E' AS index_b,
        ROUND(CORR(fchi, stoxx50e)::numeric, 2) AS correlation
    FROM
        public.stock_data
)

SELECT * FROM nasdaq_gspc_correlation
UNION ALL
SELECT * FROM nasdaq_dji_correlation
UNION ALL
SELECT * FROM gspc_dji_correlation
UNION ALL
SELECT * FROM cac40_stoxx50_correlation