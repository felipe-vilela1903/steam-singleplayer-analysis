import pandas as pd

from conexao import criar_engine


def carregar_analise():
    engine = criar_engine()
    return pd.read_sql("SELECT * FROM analysis_games", engine)


if __name__ == "__main__":
    df = carregar_analise()
    print(df.shape)
    print(df.dtypes)
    print(df["so_single"].value_counts())