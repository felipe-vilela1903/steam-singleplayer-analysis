from datetime import date
from pathlib import Path
import json
import requests

URL = "https://steamspy.com/api.php"

pasta = Path("data/raw/steamspy") / date.today().isoformat()
pasta.mkdir(parents=True, exist_ok=True)
resp = requests.get(URL, params={"request": "all", "page": 0}, timeout=30)
resp.raise_for_status()
data = resp.json()
caminho = pasta / "all_page_0.json"

with open(caminho, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"{len(data)} jogos salvos em {caminho}")