import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

from conexao import criar_engine

PASTA = Path("data/raw/appdetails")


def ler_arquivo(arq):
    appid = int(arq.stem)
    dados = json.loads(arq.read_text(encoding="utf-8"))
    quando = datetime.fromtimestamp(arq.stat().st_mtime, tz=timezone.utc)
    return {
        "appid": appid,
        "collected_at": quando,
        "payload": json.dumps(dados[str(appid)], ensure_ascii=False),
    }


def inserir(engine, linhas):
    sql = text(
        "INSERT INTO raw_appdetails (appid, collected_at, payload) "
        "VALUES (:appid, :collected_at, CAST(:payload AS JSONB)) "
        "ON CONFLICT (appid) DO NOTHING"
    )
    with engine.begin() as conn:
        conn.execute(sql, linhas)


if __name__ == "__main__":
    arquivos = sorted(PASTA.glob("*.json"))
    linhas = [ler_arquivo(a) for a in arquivos]
    inserir(criar_engine(), linhas)
    print(f"{len(linhas)} arquivos enviados")