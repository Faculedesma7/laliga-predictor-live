import streamlit as st
import requests
import pandas as pd

API_KEY = "33247bdd475582ecc4324a1l6254a287"  # Esta funciona
URL = "https://v3.football.api-sports.io/standings?league=140&season=2023"

def obtener_tabla():
    headers = {
        "x-apisports-key": API_KEY
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
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
                    "GC": equipo["all"]["goals"]["against"]
                })
            return pd.DataFrame(tabla)
        except Exception as e:
            st.error("Error al procesar la tabla. Intentá más tarde.")
            return None
    else:
        st.error("No se pudo cargar la tabla. Verificá tu API Key o espera unos minutos.")
        return None

st.title("⚽ La Liga Predictor (2023/24)")
tabla = obtener_tabla()

if tabla is not None:
    st.dataframe(tabla)

    st.subheader("📊 Predicción de partido")
    equipo1 = st.selectbox("Elegí el primer equipo", tabla["Equipo"])
    equipo2 = st.selectbox("Elegí el segundo equipo", tabla["Equipo"])

    if equipo1 and equipo2 and equipo1 != equipo2:
        datos1 = tabla[tabla["Equipo"] == equipo1].iloc[0]
        datos2 = tabla[tabla["Equipo"] == equipo2].iloc[0]

        score1 = datos1["Puntos"] + datos1["GF"] - datos1["GC"]
        score2 = datos2["Puntos"] + datos2["GF"] - datos2["GC"]

        if score1 > score2:
            pred = f"Gana {equipo1}"
        elif score2 > score1:
            pred = f"Gana {equipo2}"
        else:
            pred = "Empate"

        st.markdown(f"**Resultado estimado:** {pred}")
    elif equipo1 == equipo2:
        st.warning("Elegí dos equipos distintos.")

