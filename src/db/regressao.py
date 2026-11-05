import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from carregar_analise import carregar_analise


def preparar(df):
    df = df.copy()
    df["nota"] = df["pct_positivo"] * 100
    df["so_single_num"] = df["so_single"].astype(int)
    df["popularidade"] = np.where(
        df["owners_ordem"] >= 7, "7+", df["owners_ordem"].astype(str)
    )
    df["preco"] = pd.cut(
        df["price_cents"],
        bins=[-1, 0, 999, 1999, 10**9],
        labels=["1 gratuito", "2 ate 9,99", "3 de 10 a 19,99", "4 de 20 em diante"],
    ).astype(str)
    df = df.dropna(subset=["ano_lancamento"])
    df["epoca"] = pd.cut(
        df["ano_lancamento"],
        bins=[0, 2014, 2019, 3000],
        labels=["1 ate 2014", "2 de 2015 a 2019", "3 de 2020 em diante"],
    ).astype(str)
    return df


def ajustar(df):
    simples = smf.ols("nota ~ so_single_num", data=df).fit(cov_type="HC3")
    ajustado = smf.ols(
        "nota ~ so_single_num + C(popularidade) + C(preco) + C(epoca)", data=df
    ).fit(cov_type="HC3")
    return simples, ajustado


def resumo(rotulo, modelo):
    ic = modelo.conf_int().loc["so_single_num"]
    return (
        f"{rotulo}: {modelo.params['so_single_num']:.1f} pontos "
        f"(IC 95%: {ic[0]:.1f} a {ic[1]:.1f})"
    )


if __name__ == "__main__":
    base = carregar_analise()
    for corte in [100, 200]:
        df = preparar(base[base["avaliacoes"] >= corte])
        simples, ajustado = ajustar(df)
        print(f"--- corte de {corte} avaliações: {int(ajustado.nobs)} jogos")
        print(resumo("sem controles", simples))
        print(resumo("com controles", ajustado))