-- models/cumulative_interest.sql

WITH interest_rates AS (
    SELECT
        Date,
        USA,
        Japon,
        France,
        Europe
    FROM public.interest_rates
),

log_interest AS (
    SELECT
        Date,
        LN(1 + USA/100.0) AS Log_USA,
        LN(1 + Japon/100.0) AS Log_Japon,
        LN(1 + France/100.0) AS Log_France,
        LN(1 + Europe/100.0) AS Log_Europe
    FROM interest_rates
),

cumulative_log_interest AS (
    SELECT
        Date,
        SUM(Log_USA) OVER (ORDER BY Date) AS Cumulative_Log_USA,
        SUM(Log_Japon) OVER (ORDER BY Date) AS Cumulative_Log_Japon,
        SUM(Log_France) OVER (ORDER BY Date) AS Cumulative_Log_France,
        SUM(Log_Europe) OVER (ORDER BY Date) AS Cumulative_Log_Europe
    FROM log_interest
)

SELECT
    Date,
    ROUND(((EXP(Cumulative_Log_USA) - 1) * 100)::numeric, 2) AS Cumulative_interest_USA,
    ROUND(((EXP(Cumulative_Log_Japon) - 1) * 100)::numeric, 2) AS Cumulative_interest_Japon,
    ROUND(((EXP(Cumulative_Log_France) - 1) * 100)::numeric, 2) AS Cumulative_interest_France,
    ROUND(((EXP(Cumulative_Log_Europe) - 1) * 100)::numeric, 2) AS Cumulative_interest_Europe
FROM cumulative_log_interest
ORDER BY Date