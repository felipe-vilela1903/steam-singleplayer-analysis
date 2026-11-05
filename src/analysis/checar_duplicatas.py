import json
from collections import Counter
from pathlib import Path

pasta = Path("data/raw/steamspy/2026-11-05")
arquivos = sorted(
    pasta.glob("all_page_*.json"),
    key=lambda p: int(p.stem.split("_")[-1]),
)

contador = Counter()
total = 0
for arq in arquivos:
    data = json.loads(arq.read_text(encoding="utf-8"))
    total += len(data)
    for jogo in data.values():
        contador[jogo["appid"]] += 1

print("páginas lidas:", len(arquivos))
print("entradas no total:", total)
print("appids distintos:", len(contador))
print("appids repetidos:", sum(1 for c in contador.values() if c > 1))
print("appid 999999 (escondidos):", contador.get(999999, 0))