import streamlit as st
import pandas as pd
import pydeck as pdk
import time

CSV_FILE = "data/realtime/ais_data_raw_rt.csv"
REFRESH_SEC = 10

# Bounding box Stretto di Sicilia [lon, lat]
BBOX_POLYGON = [[
    [9.5017912796,  32.3531186757],
    [19.4354646574, 32.3531186757],
    [19.4354646574, 39.1207367613],
    [9.5017912796,  39.1207367613],
    [9.5017912796,  32.3531186757],
]]

st.set_page_config(page_title="AIS Stretto di Sicilia", layout="wide")
st.title("AIS — Stretto di Sicilia")

try:
    df = pd.read_csv(CSV_FILE)
    df = df.dropna(subset=["latitude", "longitude"])

    st.metric("Navi rilevate", df["mmsi"].nunique())

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_color=[255, 0, 0, 180],
        get_radius=500,
        pickable=True,
    )

    bbox_layer = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": BBOX_POLYGON}],
        get_polygon="polygon",
        get_fill_color=[0, 0, 255, 30],
        get_line_color=[0, 0, 255, 200],
        get_line_width=3000,
        stroked=True,
        filled=True,
    )

    view = pdk.ViewState(
        latitude=35.74,
        longitude=14.47,
        zoom=5,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[bbox_layer, scatter_layer],
        initial_view_state=view,
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
    ))

except FileNotFoundError:
    st.error(f"File non trovato: {CSV_FILE}")

time.sleep(REFRESH_SEC)
st.rerun()
