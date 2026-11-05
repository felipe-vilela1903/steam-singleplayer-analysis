# Decisões do projeto

## 1. Fonte da métrica de avaliação
- Decisão: usar `positive` e `negative` do SteamSpy para calcular o % de avaliações positivas.
- Por quê: a documentação do endpoint `all` não lista esses campos, mas a resposta real os traz. Prefiro essa fração ao `userscore`, que veio 0 no CS:GO e parece pouco confiável.

## 2. Coleta em páginas, com a data na pasta
- Decisão: o script salva cada página num arquivo próprio, dentro de uma pasta com a data da coleta, e pula as páginas que já foram baixadas.
- Por quê: a documentação do SteamSpy diz que os dados são atualizados uma vez por dia, então repetir o pedido no mesmo dia não traz nada de novo. O endpoint `all` aceita 1 pedido a cada 60 segundos, por isso o script espera 61 segundos entre as páginas baixadas.

## 3. Gravação segura dos arquivos
- Decisão: o script grava primeiro num arquivo temporário (`.tmp`) e só renomeia para `.json` quando a gravação termina.
- Por quê: se o programa for interrompido no meio da gravação, o arquivo ficaria incompleto e a próxima execução o pularia, achando que estava pronto. Com o `.tmp`, o arquivo final nunca fica pela metade.

## 4. Filtro mínimo de avaliações (a confirmar na limpeza)
- Decisão provisória: só analisar jogos com pelo menos 50 avaliações.
- Por quê: um jogo com 3 avaliações, todas positivas, teria 100% de aprovação, mas isso é ruído e não sinal. O valor de 50 é um ponto de partida e vou testar a sensibilidade da análise a ele.

## 5. Pontos de atenção nos dados
- `owners` vem como texto com faixa (por exemplo, `100,000,000 .. 200,000,000`), não como número.
- `price` vem como texto, e `positive` e `negative` vêm como número.
- `average_forever` veio 0 no CS:GO, mesmo com milhões de donos, então vou checar quantos jogos têm esse campo zerado antes de usá-lo.
- O `all` vem ordenado por número de donos, e as primeiras posições são jogos gigantes e multiplayer. Por isso preciso de todas as páginas, e não só das primeiras.
- `tags`, `genre`, `languages`, data de lançamento e a informação de single player não vêm no `all`. Vou precisar de uma segunda fase de coleta, com os detalhes de cada jogo que passar no filtro.

## 6. Jogos repetidos entre páginas
- Observação: na checagem das páginas 0 a 49, 4.042 appids apareciam em mais de uma página do `all` (cerca de 8% das 50.000 entradas). Todas as cópias eram idênticas, e quase todas (3.827) estavam em páginas vizinhas.
- Decisão: a chave `(appid, collected_date)` mantém uma linha por jogo, e a carga ignora as repetições com `ON CONFLICT DO NOTHING`.
- Limitação: a hipótese é que a ordenação do `all` mude entre um pedido e outro, o que também pode ter deixado alguns jogos fora de todas as páginas. Não consigo medir os que nunca apareceram. Os números serão atualizados quando a coleta terminar.