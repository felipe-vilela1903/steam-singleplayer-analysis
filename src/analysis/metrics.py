def pct_positivo(jogo):
    total = jogo['positive'] + jogo['negative']
    if total == 0:
        return None
    return jogo['positive'] / total
    