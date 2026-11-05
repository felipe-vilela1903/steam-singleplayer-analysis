import json
from collections import Counter
from pathlib import Path

pasta = Path("data/raw/steamspy/2026-11-05")
arquivos = sorted(
    pasta.glob("all_page_*.json"),
    key=lambda p: int(p.stem.split("_")[-1]),
)

primeira = {}
iguais = 0
diferentes = 0
distancias = Counter()

for arq in arquivos:
    pagina = int(arq.stem.split("_")[-1])
    data = json.loads(arq.read_text(encoding="utf-8"))
    for jogo in data.values():
        appid = jogo["appid"]
        if appid in primeira:
            pag_ant, jogo_ant = primeira[appid]
            if jogo == jogo_ant:
                iguais += 1
            else:
                diferentes += 1
            distancias[pagina - pag_ant] += 1
        else:
            primeira[appid] = (pagina, jogo)

print("repetidos idênticos:", iguais)
print("repetidos com valores diferentes:", diferentes)
print("distância entre páginas (distância: quantidade):")
for d, q in sorted(distancias.items())[:10]:
    print(d, q)