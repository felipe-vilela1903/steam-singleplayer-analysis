import json
import time
from pathlib import Path

import requests

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


for appid in [730, 413150, 999999999]:
    print(appid, baixar_detalhes(appid))
    time.sleep(2)