import streamlit as st
import requests
import pandas as pd

import streamlit as st

API_KEY = st.secrets["api"]["key"]
 # 🔁 Reemplazá esto con tu API key real

headers = {
    "x-apisports-key": API_KEY
}

# Obtener tabla de posiciones actual
def obtener_tabla():
    url = "https://v3.football.api-sports.io/standings?league=140&season=2024"
    response = requests.get(url, headers=headers)
    data = response.json()
    equipos = data["response"][0]["league"]["standings"][0]
    tabla = []
    for equipo in equipos:
        tabla.append({
            "Posición": equipo["rank"],
            "Equipo": equipo["team"]["name"],
            "Puntos": equipo["points"],
            "PJ": equipo["all"]["played"],
            "PG": equipo["all"]["win"],
            "PE": equipo["all"]["draw"],
            "PP": equipo["all"]["lose"],
            "GF": equipo["all"]["goals"]["for"],
            "GC": equipo["all"]["goals"]["against"],
            "DIF": equipo["goalsDiff"]
        })
    return pd.DataFrame(tabla)

# Predicción simple según puntos
def predecir_ganador(equipo1, equipo2, df):
    puntos1 = df[df["Equipo"] == equipo1]["Puntos"].values[0]
    puntos2 = df[df["Equipo"] == equipo2]["Puntos"].values[0]
    if puntos1 > puntos2:
        return f"Gana {equipo1} ✅"
    elif puntos2 > puntos1:
        return f"Gana {equipo2} ✅"
    else:
        return "Empate 🤝"

st.title("⚽ La Liga Predictor (2024/25)")
st.write("Datos en vivo de la tabla y predicción entre equipos")

tabla = obtener_tabla()
st.dataframe(tabla)

st.subheader("🔮 ¿Quién ganaría un partido?")
equipo1 = st.selectbox("Equipo 1", tabla["Equipo"])
equipo2 = st.selectbox("Equipo 2", tabla["Equipo"])

if equipo1 != equipo2:
    resultado = predecir_ganador(equipo1, equipo2, tabla)
    st.success(resultado)
else:
    st.warning("Elegí dos equipos distintos")
