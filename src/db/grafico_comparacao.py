from pathlib import Path

import matplotlib.pyplot as plt

from carregar_analise import carregar_analise

SAIDA = Path("reports/figures/comparacao_single_multi.png")

df = carregar_analise()
df["nota"] = df["pct_positivo"] * 100

grupos = [
    ("só single player", df[df["so_single"]]["nota"]),
    ("single + multi", df[~df["so_single"]]["nota"]),
]

fig, ax = plt.subplots(figsize=(6, 5))
for i, (rotulo, notas) in enumerate(grupos):
    media = notas.mean()
    erro = notas.std() / len(notas) ** 0.5
    ax.errorbar(i, media, yerr=2 * erro, fmt="o", capsize=6)
    ax.annotate(
        f"{media:.1f}%\n(n = {len(notas)})",
        (i, media),
        textcoords="offset points",
        xytext=(14, -6),
    )
    print(f"{rotulo}: {media:.1f} ± {2 * erro:.1f}")

ax.set_xticks([0, 1])
ax.set_xticklabels([rotulo for rotulo, _ in grupos])
ax.set_xlim(-0.6, 1.6)
ax.set_ylabel("média de % de avaliações positivas")
ax.set_title("Média das notas e intervalo aproximado (± 2 erros padrão)")

SAIDA.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(SAIDA, dpi=150, bbox_inches="tight")
print(f"salvo em {SAIDA}")