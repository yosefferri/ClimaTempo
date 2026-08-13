import requests

def buscar_clima(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "hourly": "precipitation_probability",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1
    }
    resposta = requests.get(url, params=parametros)
    return resposta.json()