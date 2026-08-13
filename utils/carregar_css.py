def carregar_css(caminho_arquivo):
    with open(caminho_arquivo) as f:
        return f.read()