import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="La Liga Predictor Avanzado", layout="wide")
st.title("⚽ La Liga - Predicción en Vivo y Detallada")

# Temporada seleccionada
season = st.selectbox("Seleccioná la temporada:", ["2024", "2023", "2022", "2021"])

st.subheader(f"📊 Tabla de posiciones - Temporada {season}")

@st.cache_data
def obtener_tabla(season):
    try:
        url = "https://zylalabs.com/api/857/la+liga+table+api/635/obtain+la+liga+table"
        params = {"season": season}
        response = requests.get(url, params=params)
        data = response.json()

        tabla = []
        for team in data:
            tabla.append({
                "Pos": team["position"],
                "Equipo": team["team"]["name"],
                "PJ": team["stats"]["played"],
                "G": team["stats"]["wins"],
                "E": team["stats"]["draws"],
                "P": team["stats"]["loses"],
                "GF": team["stats"]["goalsFor"],
                "GC": team["stats"]["goalsAgainst"],
                "DG": team["stats"]["goalsFor"] - team["stats"]["goalsAgainst"],
                "Pts": team["stats"]["points"]
            })

        df = pd.DataFrame(tabla)
        df = df.sort_values(by="Pos")
        return df
    except:
        return None

# Mostrar tabla
tabla = obtener_tabla(season)
if tabla is not None and not tabla.empty:
    st.dataframe(tabla, use_container_width=True)
else:
    st.error("No se pudo cargar la tabla. Intentá más tarde o probá con otra temporada.")

st.subheader("🤖 ¿Quién tiene más chances de ganar?")
equipos = tabla["Equipo"].tolist() if tabla is not None else []

col1, col2 = st.columns(2)
with col1:
    equipo1 = st.selectbox("Equipo 1", equipos)
with col2:
    equipo2 = st.selectbox("Equipo 2", equipos, index=1 if len(equipos) > 1 else 0)

if equipo1 != equipo2:
    equipo1_stats = tabla[tabla["Equipo"] == equipo1].iloc[0]
    equipo2_stats = tabla[tabla["Equipo"] == equipo2].iloc[0]

    st.markdown("### 🔍 Comparación detallada")
    comparacion = pd.DataFrame({
        "Estadística": ["Puntos", "Partidos Jugados", "Victorias", "Empates", "Derrotas", "Goles a Favor", "Goles en Contra", "Diferencia de Gol"],
        equipo1: [
            equipo1_stats["Pts"], equipo1_stats["PJ"], equipo1_stats["G"], equipo1_stats["E"], equipo1_stats["P"],
            equipo1_stats["GF"], equipo1_stats["GC"], equipo1_stats["DG"]
        ],
        equipo2: [
            equipo2_stats["Pts"], equipo2_stats["PJ"], equipo2_stats["G"], equipo2_stats["E"], equipo2_stats["P"],
            equipo2_stats["GF"], equipo2_stats["GC"], equipo2_stats["DG"]
        ]
    })
    st.dataframe(comparacion, use_container_width=True)

    st.markdown("### 🔮 Predicción")
    puntaje1 = equipo1_stats["Pts"] + equipo1_stats["DG"] * 0.2 + equipo1_stats["GF"] * 0.1
    puntaje2 = equipo2_stats["Pts"] + equipo2_stats["DG"] * 0.2 + equipo2_stats["GF"] * 0.1

    if puntaje1 > puntaje2:
        st.success(f"{equipo1} tiene más chances de ganar 🏆")
    elif puntaje2 > puntaje1:
        st.success(f"{equipo2} tiene más chances de ganar 🏆")
    else:
        st.info("Es un partido muy parejo. Puede ser empate.")
else:
    st.warning("Elegí dos equipos distintos.")

