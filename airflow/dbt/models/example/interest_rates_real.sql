-- models/interest_real.sql

WITH inflation_rates AS (
    SELECT * FROM public.inflation_rates
),

interest_rates AS (
    SELECT * FROM public.interest_rates
)

SELECT
    ir.Date,
    ROUND(((1 + ir.USA) / (1 + inf.USA) - 1)::numeric, 2) AS USA,
    ROUND(((1 + ir.Japon) / (1 + inf.Japon) - 1)::numeric, 2) AS Japon,
    ROUND(((1 + ir.France) / (1 + inf.France) - 1)::numeric, 2) AS France,
    ROUND(((1 + ir.Europe) / (1 + inf.Europe) - 1)::numeric, 2) AS Europe
FROM
    interest_rates ir
JOIN
    inflation_rates inf ON ir.Date = inf.Date
