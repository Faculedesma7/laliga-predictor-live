import streamlit as st
import requests

st.set_page_config(page_title="La Liga Predictor", layout="wide")

st.title("⚽ La Liga - Tabla de posiciones (2024/25)")

# API gratuita desde API-SPORTS
api_key = "33247bdd475582ecc4324a1l6254a287"
url = "https://v3.football.api-sports.io/standings?league=140&season=2024"

headers = {
    "x-apisports-key": api_key
}

response = requests.get(url, headers=headers)
data = response.json()

try:
    equipos = data["response"][0]["league"]["standings"][0]

    tabla = []
    for equipo in equipos:
        tabla.append([
            equipo["rank"],
            equipo["team"]["name"],
            equipo["points"],
            equipo["all"]["win"],
            equipo["all"]["draw"],
            equipo["all"]["lose"]
        ])

    st.table(tabla)

except Exception as e:
    st.error("No se pudo cargar la tabla. Verificá tu API Key o espera unos minutos.")
    st.warning("Elegí dos equipos distintos")
