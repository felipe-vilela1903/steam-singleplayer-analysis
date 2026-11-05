# Jogos single player na Steam: o que explica uma boa avaliação?

> 🚧 Projeto em andamento: a coleta, o banco e a primeira análise estão prontos. Os próximos passos são os gêneros e um dashboard em Power BI.

## A pergunta
Quis entender o que diferencia os jogos single player bem avaliados na Steam. Coletei os dados por API, guardei num PostgreSQL e analisei em SQL e Python.

## O que encontrei até agora
- Numa amostra sorteada de 927 jogos, a nota média (% de avaliações positivas) é 79,5% e a mediana é 83,0%. A distribuição tem uma cauda longa para as notas baixas.
- Os jogos sem modo multijogador têm nota maior que os que também têm: 80,4% contra 76,8% em média. Mantendo popularidade, preço e época de lançamento fixos, a diferença estimada é de 4,6 pontos (intervalo de 95%: 2,3 a 7,0).
- Isso descreve a amostra. Não mostra que o multijogador causa a diferença.

![Distribuição das notas](reports/figures/distribuicao_notas.png)

![Comparação entre os dois grupos](reports/figures/comparacao_single_multi.png)