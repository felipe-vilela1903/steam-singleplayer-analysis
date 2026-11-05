-- 1. Distribuição das notas (faixas de 10 pontos)
SELECT LEAST(FLOOR(pct_positivo * 10), 9) / 10 AS faixa_inicio, COUNT(*) AS jogos
FROM analysis_games GROUP BY 1 ORDER BY 1;

-- 2. Nota por faixa de popularidade (owners_ordem)
SELECT owners_ordem, COUNT(*) AS jogos,
       ROUND(AVG(pct_positivo), 3) AS media_pct,
       ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pct_positivo))::numeric, 3) AS mediana_pct
FROM analysis_games GROUP BY owners_ordem ORDER BY owners_ordem;

-- 3. Nota por faixa de preço (preço atual, em centavos de dólar)
SELECT CASE
           WHEN price_cents = 0    THEN '1 gratuito'
           WHEN price_cents < 1000 THEN '2 até US$ 9,99'
           WHEN price_cents < 2000 THEN '3 US$ 10 a 19,99'
           WHEN price_cents < 3000 THEN '4 US$ 20 a 29,99'
           ELSE                         '5 US$ 30 ou mais'
       END AS faixa_preco,
       COUNT(*) AS jogos,
       ROUND(AVG(pct_positivo), 3) AS media_pct,
       ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pct_positivo))::numeric, 3) AS mediana_pct
FROM analysis_games GROUP BY 1 ORDER BY 1;

-- 4. Nota por época de lançamento (cortes arbitrários)
SELECT CASE
           WHEN ano_lancamento IS NULL  THEN '0 sem data'
           WHEN ano_lancamento <= 2009  THEN '1 até 2009'
           WHEN ano_lancamento <= 2014  THEN '2 de 2010 a 2014'
           WHEN ano_lancamento <= 2019  THEN '3 de 2015 a 2019'
           WHEN ano_lancamento <= 2024  THEN '4 de 2020 a 2024'
           ELSE                              '5 de 2025 em diante'
       END AS epoca,
       COUNT(*) AS jogos,
       ROUND(AVG(pct_positivo), 3) AS media_pct,
       ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pct_positivo))::numeric, 3) AS mediana_pct
FROM analysis_games GROUP BY 1 ORDER BY 1;

-- 5. Só single player contra single + multi, com desvio e erro padrão
SELECT CASE WHEN so_single THEN 'só single player' ELSE 'single + multi' END AS grupo,
       COUNT(*) AS jogos,
       ROUND(AVG(pct_positivo), 3) AS media_pct,
       ROUND(STDDEV(pct_positivo), 3) AS desvio,
       ROUND((STDDEV(pct_positivo) / SQRT(COUNT(*)))::numeric, 4) AS erro_padrao
FROM analysis_games GROUP BY so_single ORDER BY so_single DESC;

-- 6. A mesma comparação dentro de cada faixa de popularidade (faixas 1 a 6)
SELECT owners_ordem,
       CASE WHEN so_single THEN 'só single' ELSE 'single + multi' END AS grupo,
       COUNT(*) AS jogos,
       ROUND(AVG(pct_positivo), 3) AS media_pct
FROM analysis_games WHERE owners_ordem <= 6
GROUP BY owners_ordem, so_single ORDER BY owners_ordem, so_single DESC;