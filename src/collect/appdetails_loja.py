import json
import time
from pathlib import Path

import requests
import sys

URL = "https://store.steampowered.com/api/appdetails"
PASTA = Path("data/raw/appdetails")
PASTA.mkdir(parents=True, exist_ok=True)


def baixar_detalhes(appid):
    caminho = PASTA / f"{appid}.json"
    if caminho.exists():
        return None

    resp = requests.get(URL, params={"appids": appid, "l": "english"}, timeout=30)
    resp.raise_for_status()
    dados = resp.json()

    temporario = caminho.with_suffix(".tmp")
    with open(temporario, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    temporario.replace(caminho)

    return dados[str(appid)]["success"]


def ler_amostra():
    caminho = Path("data/processed/amostra_appids.txt")
    return [int(linha) for linha in caminho.read_text(encoding="utf-8").split()]


if __name__ == "__main__":
    baixados = 0
    for appid in ler_amostra():
        try:
            resultado = baixar_detalhes(appid)
        except requests.RequestException as erro:
            print(f"erro no appid {appid}: {erro}")
            sys.exit(1)
        if resultado is not None:
            baixados += 1
            if baixados % 50 == 0:
                print(f"{baixados} baixados...")
            time.sleep(2)
    print(f"baixados nesta execução: {baixados}")