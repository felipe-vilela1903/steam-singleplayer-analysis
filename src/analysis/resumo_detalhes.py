import json
from collections import Counter
from pathlib import Path

pasta = Path("data/raw/appdetails")
contagem = Counter()

for arq in sorted(pasta.glob("*.json")):
    dados = json.loads(arq.read_text(encoding="utf-8"))
    entrada = dados[arq.stem]
    if not entrada["success"]:
        contagem["sem dados (success=False)"] += 1
        continue
    info = entrada["data"]
    contagem[f"type={info['type']}"] += 1
    categorias = [c["description"] for c in info.get("categories", [])]
    if "Single-player" in categorias:
        contagem["tem Single-player"] += 1
        if "Multi-player" not in categorias:
            contagem["só single player"] += 1

for chave, qtd in sorted(contagem.items()):
    print(chave, qtd)