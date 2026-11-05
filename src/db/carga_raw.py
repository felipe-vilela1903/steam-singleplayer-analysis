import json
from datetime import date
from pathlib import Path

from sqlalchemy import text

from conexao import criar_engine

COLUNAS = [
    "appid", "name", "developer", "publisher", "score_rank",
    "positive", "negative", "userscore", "owners",
    "average_forever", "average_2weeks", "median_forever", "median_2weeks",
    "ccu", "price", "initialprice", "discount",
]


def linhas_da_pagina(data, data_coleta):
    linhas = []
    for jogo in data.values():
        linha = {col: jogo.get(col) for col in COLUNAS}
        linha["collected_date"] = data_coleta
        linhas.append(linha)
    return linhas


def inserir(engine, linhas):
    todas = COLUNAS + ["collected_date"]
    colunas_sql = ", ".join(todas)
    parametros = ", ".join(f":{c}" for c in todas)
    sql = text(
        f"INSERT INTO raw_steamspy ({colunas_sql}) "
        f"VALUES ({parametros}) "
        "ON CONFLICT (appid, collected_date) DO NOTHING"
    )
    with engine.begin() as conn:
        conn.execute(sql, linhas)


def carregar_pasta(engine, pasta):
    data_coleta = date.fromisoformat(pasta.name)
    arquivos = sorted(
        pasta.glob("all_page_*.json"),
        key=lambda p: int(p.stem.split("_")[-1]),
    )
    total = 0
    for arq in arquivos:
        data = json.loads(arq.read_text(encoding="utf-8"))
        linhas = linhas_da_pagina(data, data_coleta)
        inserir(engine, linhas)
        total += len(linhas)
        print(f"{arq.name}: {len(linhas)} linhas")
    print(f"total enviado: {total}")


if __name__ == "__main__":
    carregar_pasta(criar_engine(), Path("data/raw/steamspy/2026-11-05"))