from datetime import date
from pathlib import Path
import json
import requests

URL = "https://steamspy.com/api.php"

pasta = Path("data/raw/steamspy") / date.today().isoformat()
pasta.mkdir(parents=True, exist_ok=True)


def baixar_pagina(pagina):
    caminho = pasta / f"all_page_{pagina}.json"
    if caminho.exists():
        return None

    resp = requests.get(URL, params={"request": "all", "page": pagina}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"{len(data)} jogos salvos em {caminho}")
    return len(data)

print(baixar_pagina(0))
print(baixar_pagina(1))