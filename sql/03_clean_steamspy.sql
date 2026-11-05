CREATE VIEW clean_steamspy AS
SELECT
    r.appid,
    r.name,
    r.positive,
    r.negative,
    r.positive + r.negative AS avaliacoes,
    r.positive::numeric / NULLIF(r.positive + r.negative, 0) AS pct_positivo,
    f.ordem AS owners_ordem,
    CASE WHEN r.price ~ '^[0-9]+$' THEN r.price::integer END AS price_cents
FROM raw_steamspy r
JOIN owners_faixas f ON f.faixa = r.owners
WHERE r.positive + r.negative >= 100;