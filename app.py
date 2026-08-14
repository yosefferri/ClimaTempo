import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_geocoding import buscar_cidade
from utils.api_clima import buscar_clima

cidades_fixas = {
    "Jaú": (-22.29639, -48.55778),
    "São Paulo": (-23.5505, -46.6333),
    "Nova Iorque": (40.7128, -74.0060),
    "Londres": (51.5074, -0.1278),
    "Pequim": (39.9042, 116.4074),
    "Moscou": (55.7558, 37.6173)
}

st.set_page_config(page_title="Clima em Tempo Real")


st.title("🌤️ Clima em Tempo Real")
st.caption("Consulta ao vivo via API Open-Meteo — dados atualizados a cada busca.")
st.divider()

st.subheader("Clima nas principais cidades")

lista_cidades = list(cidades_fixas.items())

# ---------- Linha 1: só Jaú ----------
nome_cidade, coordenadas = lista_cidades[0]
latitude_fixa, longitude_fixa = coordenadas
dados_fixos = buscar_clima(latitude_fixa, longitude_fixa)

if "current" in dados_fixos:
    st.metric(
        nome_cidade,
        f"{dados_fixos['current']['temperature_2m']} °C",
        f"{dados_fixos['current']['relative_humidity_2m']}% umidade"
    )
else:
    st.warning(f"Não foi possível carregar {nome_cidade}")

st.write("")

# ---------- Linha 2: as outras 5 cidades ---------
colunas_linha2 = st.columns(5)
for i in range(1, 6):
    nome_cidade, coordenadas = lista_cidades[i]
    latitude_fixa, longitude_fixa = coordenadas
    dados_fixos = buscar_clima(latitude_fixa, longitude_fixa)

    with colunas_linha2[i - 1]:
        if "current" in dados_fixos:
            st.metric(
                nome_cidade,
                f"{dados_fixos['current']['temperature_2m']} °C",
                f"{dados_fixos['current']['relative_humidity_2m']}% umidade"
            )
        else:
            st.warning(f"Não foi possível carregar {nome_cidade}")
st.write("")

def carregar_css(caminho_arquivo):
    with open(caminho_arquivo) as f:
        return f.read()

css = carregar_css("style/custom.css")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

nome_digitado = st.text_input("Digite o nome da cidade")

if nome_digitado:
    resultados = buscar_cidade(nome_digitado)

    if "results" in resultados:
        opcoes = [f"{r['name']}, {r['admin1']}, {r['country']}" for r in resultados["results"]]
        cidade_escolhida = st.selectbox("Se caso não for a cidade correta, clique aqui abaixo: ", opcoes)

        indice = opcoes.index(cidade_escolhida)
        latitude = resultados["results"][indice]["latitude"]
        longitude = resultados["results"][indice]["longitude"]


        from datetime import datetime

        dados_clima = buscar_clima(latitude, longitude)

        if "current" in dados_clima:
            # ---------- Parte 1: as métricas de agora ----------
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Temperatura", f"{dados_clima['current']['temperature_2m']} °C")
            col2.metric("Umidade", f"{dados_clima['current']['relative_humidity_2m']}%")
            col3.metric("Vento", f"{dados_clima['current']['wind_speed_10m']} km/h")
            col4.metric("Chuva agora", f"{dados_clima['current']['precipitation']} mm")

            # ---------- Parte 2: seu código de probabilidade (o que você já tinha) ----------
            agora = datetime.now().strftime("%Y-%m-%dT%H:00")

            lista_horarios = dados_clima["hourly"]["time"]
            lista_probabilidades = dados_clima["hourly"]["precipitation_probability"]

            if agora in lista_horarios:
                indice_agora = lista_horarios.index(agora)
                probabilidade_chuva = lista_probabilidades[indice_agora]
            else:
                probabilidade_chuva = "Nenhuma"

            col5.metric("Chance de chuva", f"{probabilidade_chuva}%")

            # ---------- Parte 3: o gráfico de previsão ----------
            st.subheader("Previsão de chuva para hoje")

            df_previsao = pd.DataFrame({
                "hora": dados_clima["hourly"]["time"],
                "probabilidade": dados_clima["hourly"]["precipitation_probability"]
            })

            fig_previsao = px.line(
                df_previsao,
                x="hora",
                y="probabilidade",
                labels={"hora": "Hora", "probabilidade": "Chance de chuva (%)"}
            )

            st.plotly_chart(fig_previsao, use_container_width=True, key="grafico_previsao_chuva")

        else:
            st.warning("Não foi possível carregar os dados dessa cidade no momento. Tente novamente em instantes.")


st.divider()
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 14px; padding-top: 10px;">
        © 2026 Ferri — Dashboard de Clima em Tempo Real<br>
        Feito com Python, Streamlit e Plotly · Dados via Open-Meteo API<br>
        Contato: joseferri225@gmail.com · <a href="https://github.com/yosefferri/ClimaTempo" style="color: gray;" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)


