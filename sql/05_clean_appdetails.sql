CREATE VIEW clean_appdetails AS
SELECT
    appid,
    tipo,
    CASE
        WHEN d ~ '^[0-9]{1,2} [A-Za-z]{3}, [0-9]{4}$' THEN to_date(d, 'DD Mon, YYYY')
        WHEN d ~ '^[A-Za-z]{3} [0-9]{1,2}, [0-9]{4}$' THEN to_date(d, 'Mon DD, YYYY')
    END AS data_lancamento,
    cat @> '[{"description": "Single-player"}]'::jsonb AS single_player,
    cat @> '[{"description": "Multi-player"}]'::jsonb AS multi_player
FROM (
    SELECT
        appid,
        payload->'data'->>'type' AS tipo,
        payload->'data'->'release_date'->>'date' AS d,
        payload->'data'->'categories' AS cat
    FROM raw_appdetails
    WHERE payload->>'success' = 'true'
) t;