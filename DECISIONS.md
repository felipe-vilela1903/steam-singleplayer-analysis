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

## 4. Filtro mínimo de avaliações
- Decisão: só analisar jogos com pelo menos 100 avaliações (positivas mais negativas).
- Por quê: com poucas avaliações, o % positivo oscila muito. Com 10, cada voto move a nota em 10 pontos, e com 100 o erro típico fica na casa de 4 pontos (conta aproximada, para um jogo com cerca de 80% de aprovação). Dos 82.502 jogos da coleta completa, 23.049 passam desse corte (28%).
- Limitação: o filtro deixa de fora jogos pouco conhecidos, então as conclusões valem para jogos com uma base mínima de jogadores. Depois da análise principal, vou repetir os resultados com cortes de 50 e de 200 para ver se as conclusões dependem desse número.

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

## 7. Definição de single player
- Decisão: considerar single player o jogo com a categoria `Single-player` na API da loja. Guardo à parte uma marca "só single player" (com `Single-player` e sem `Multi-player`), para comparar os dois grupos.
- Por quê: muitos jogos têm as duas categorias. Em 300 jogos sorteados, 281 têm `Single-player` e 77 deles também têm `Multi-player`. Excluí-los mudaria a pergunta do projeto, e tratá-los todos iguais esconderia a diferença.
- Limitação: as categorias vêm do cadastro do jogo na loja e não foram verificadas uma a uma. As frações serão recalculadas com a amostra final.

## 8. Popularidade como posição de 1 a 13
- Decisão: converter `owners` na posição da faixa (1 = `0 .. 20,000`, 13 = `100,000,000 .. 200,000,000`), usando uma tabela de consulta (`owners_faixas`).
- Por quê: o campo é uma faixa de texto, e 56.472 dos 82.502 jogos (68%) estão na menor faixa. Usar o limite inferior colocaria quase 7 em cada 10 jogos em "0 donos". Cada faixa tem aproximadamente o dobro de donos da anterior, então a posição é uma medida natural de popularidade.
- Limitação: `owners` é uma estimativa do SteamSpy com faixas largas. Na análise, a nota não cresce nem cai de forma contínua com a faixa, então ela entra no modelo como categoria, e não como um número crescente.

## 9. Amostra para buscar os detalhes da loja
- Decisão: pedir os detalhes à API da loja só para uma amostra de 1.000 jogos com 100 ou mais avaliações, ordenados por `md5(appid || semente)` com a semente fixa `steam-singleplayer-v1`.
- Por quê: buscar os 23.049 jogos levaria mais de 10 horas, e ordenar por um hash dá uma amostra pseudoaleatória que qualquer pessoa reproduz. Na amostra, 994 jogos vieram com dados e 928 entraram na análise (single player e do tipo `game`), cerca de 4% dos 23.049.
- Limitação: o resultado descreve esses 928 jogos. Intervalos e diferenças são aproximados, e eu não fiz testes formais.

## 10. Data de lançamento e tipo do item
- Decisão: converter a data por um `CASE` com dois formatos (`DD Mon, YYYY` e `Mon DD, YYYY`) e filtrar `type = 'game'`.
- Por quê: a loja devolveu os dois formatos (986 e 5 jogos), mais 3 datas vazias. Na amostra de 994 itens, 1 era `demo`.
- Limitação: não sei por que o formato varia, e 2 jogos da análise ficam sem data.