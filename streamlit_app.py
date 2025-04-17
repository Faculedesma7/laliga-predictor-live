import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Predicción La Liga", layout="centered")
st.title("⚽ La Liga - Tabla y Predicción de Partidos")

# API-FOOTBALL
API_KEY = "33247bdd475582ecc4324a1l6254a287"
URL = "https://v3.football.api-sports.io/standings?league=140&season=2023"

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(URL, headers=headers)
data = response.json()

try:
    equipos = data["response"][0]["league"]["standings"][0]

    tabla = []
    nombres = []

    for equipo in equipos:
        tabla.append([
            equipo["rank"],
            equipo["team"]["name"],
            equipo["points"],
            equipo["all"]["win"],
            equipo["all"]["draw"],
            equipo["all"]["lose"]
        ])
        nombres.append(equipo["team"]["name"])

    st.subheader("📊 Tabla de posiciones 2023/24")
    st.table(tabla)

    # Predicción
    st.subheader("🔮 Predicción entre dos equipos")

    equipo1 = st.selectbox("Elegí el primer equipo", nombres, key="e1")
    equipo2 = st.selectbox("Elegí el segundo equipo", [e for e in nombres if e != equipo1], key="e2")

    datos_e1 = next(e for e in equipos if e["team"]["name"] == equipo1)
    datos_e2 = next(e for e in equipos if e["team"]["name"] == equipo2)

    puntos1 = datos_e1["points"]
    puntos2 = datos_e2["points"]

    st.write(f"**{equipo1}** tiene {puntos1} puntos.")
    st.write(f"**{equipo2}** tiene {puntos2} puntos.")

    if puntos1 > puntos2:
        st.success(f"✅ {equipo1} tiene más chances de ganar.")
    elif puntos2 > puntos1:
        st.success(f"✅ {equipo2} tiene más chances de ganar.")
    else:
        st.warning("⚖️ Están muy parejos. Podría ser empate.")

except Exception as e:
    st.error("❌ No se pudo cargar la tabla. Revisá la API Key o intentá más tarde.")
