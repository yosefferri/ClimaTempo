import streamlit as st
import requests

@st.cache_data(ttl=600)  # guarda o resultado em cache por 600 segundos (10 min)
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
    resposta = requests.get(url, params=parametros, timeout=10)
    return resposta.json()