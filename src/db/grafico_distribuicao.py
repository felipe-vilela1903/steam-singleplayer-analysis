from pathlib import Path

import matplotlib.pyplot as plt

from carregar_analise import carregar_analise

SAIDA = Path("reports/figures/distribuicao_notas.png")

df = carregar_analise()
notas = df["pct_positivo"] * 100
media = notas.mean()
mediana = notas.median()

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(notas, bins=list(range(0, 105, 5)), edgecolor="white")
ax.axvline(media, linestyle="--", label=f"média: {media:.1f}%")
ax.axvline(mediana, linestyle=":", label=f"mediana: {mediana:.1f}%")
ax.set_xlabel("% de avaliações positivas")
ax.set_ylabel("número de jogos")
ax.set_title(f"Notas dos jogos single player da amostra (n = {len(notas)})")
ax.legend()

SAIDA.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(SAIDA, dpi=150, bbox_inches="tight")
print(f"média {media:.1f}, mediana {mediana:.1f}, salvo em {SAIDA}")