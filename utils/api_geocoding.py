import requests

def buscar_cidade(nome_cidade):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    parametros = {"name": nome_cidade, "count": 5, "language": "pt"}
    resposta = requests.get(url, params=parametros)
    return resposta.json()