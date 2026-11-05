from datetime import date
from pathlib import Path
import json
import requests
import time

URL = "https://steamspy.com/api.php"
JOGOS_POR_PAGINA = 1000

pasta = Path("data/raw/steamspy") / date.today().isoformat()
pasta.mkdir(parents=True, exist_ok=True)


def baixar_pagina(pagina):
    caminho = pasta / f"all_page_{pagina}.json"
    if caminho.exists():
        return None

    resp = requests.get(URL, params={"request": "all", "page": pagina}, timeout=30)
    resp.raise_for_status()
    try:
        data = resp.json()
    except ValueError:
        raise RuntimeError(
            f"a página {pagina} não veio em JSON: {resp.text[:80]!r}"
        )
    if not data:
        return 0

    temporario = caminho.with_suffix(".tmp")
    with open(temporario, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    temporario.replace(caminho)

    print(f"{len(data)} jogos salvos em {caminho}")
    return len(data)


def baixar_tudo(max_paginas):
    for pagina in range(max_paginas):
        n = baixar_pagina(pagina)
        if n is not None and n < JOGOS_POR_PAGINA:
            print(f"página {pagina} veio com {n} jogos: provável fim da lista")
            break
        if n is not None:
            time.sleep(61)


baixar_tudo(300)