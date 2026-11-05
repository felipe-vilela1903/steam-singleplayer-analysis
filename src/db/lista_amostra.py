from pathlib import Path

from sqlalchemy import text

from conexao import criar_engine

SEMENTE = "steam-singleplayer-v1"
MIN_AVALIACOES = 100
SAIDA = Path("data/processed/amostra_appids.txt")


def listar_appids(engine, limite):
    sql = text(
        "SELECT appid FROM raw_steamspy "
        "WHERE positive + negative >= :minimo "
        "ORDER BY md5(appid::text || :semente) "
        "LIMIT :limite"
    )
    params = {"minimo": MIN_AVALIACOES, "semente": SEMENTE, "limite": limite}
    with engine.connect() as conn:
        return [linha[0] for linha in conn.execute(sql, params)]


if __name__ == "__main__":
    appids = listar_appids(criar_engine(), 20)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text("\n".join(str(a) for a in appids), encoding="utf-8")
    print(len(appids), appids[:3])