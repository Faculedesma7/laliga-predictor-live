import streamlit as st
import requests

st.set_page_config(page_title="La Liga Predictor", layout="wide")
st.title("⚽ La Liga Predictor (Gratis y en Vivo)")

# Temporada seleccionada
season = st.selectbox("Seleccioná la temporada:", ["2024", "2023", "2022", "2021"])

st.subheader(f"📊 Tabla de posiciones - Temporada {season}")

# API gratuita de ZylaLabs
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
                "Pts": team["stats"]["points"]
            })

        return tabla
    except:
        return None

# Mostrar tabla
tabla = obtener_tabla(season)
if tabla:
    st.dataframe(tabla, use_container_width=True)
else:
    st.error("No se pudo cargar la tabla. Intentá más tarde o probá con otra temporada.")

st.subheader("🤖 ¿Quién tiene más chances de ganar?")
equipos = [fila["Equipo"] for fila in tabla] if tabla else []

col1, col2 = st.columns(2)
with col1:
    equipo1 = st.selectbox("Equipo 1", equipos)
with col2:
    equipo2 = st.selectbox("Equipo 2", equipos, index=1 if len(equipos) > 1 else 0)

if equipo1 != equipo2:
    equipo1_stats = next((e for e in tabla if e["Equipo"] == equipo1), None)
    equipo2_stats = next((e for e in tabla if e["Equipo"] == equipo2), None)

    if equipo1_stats and equipo2_stats:
        st.markdown("### 🔮 Predicción")
        if equipo1_stats["Pts"] > equipo2_stats["Pts"]:
            st.success(f"{equipo1} tiene más chances de ganar.")
        elif equipo2_stats["Pts"] > equipo1_stats["Pts"]:
            st.success(f"{equipo2} tiene más chances de ganar.")
        else:
            st.info("Es muy parejo, puede ser empate o cualquier cosa 🟰")
else:
    st.warning("Elegí dos equipos distintos.")
