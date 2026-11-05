CREATE VIEW analysis_games AS
SELECT
    s.appid,
    s.name,
    s.positive,
    s.negative,
    s.avaliacoes,
    s.pct_positivo,
    s.owners_ordem,
    s.price_cents,
    a.data_lancamento,
    EXTRACT(YEAR FROM a.data_lancamento)::int AS ano_lancamento,
    (a.single_player AND NOT a.multi_player) AS so_single
FROM clean_steamspy s
JOIN clean_appdetails a ON a.appid = s.appid
WHERE a.tipo = 'game'
  AND a.single_player;