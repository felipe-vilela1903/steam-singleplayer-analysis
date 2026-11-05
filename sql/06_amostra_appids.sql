CREATE TABLE amostra_appids AS
SELECT appid
FROM raw_steamspy
WHERE positive + negative >= 100
ORDER BY md5(appid::text || 'steam-singleplayer-v1')
LIMIT 1000;