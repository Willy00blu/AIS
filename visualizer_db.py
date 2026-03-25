import streamlit as st
import pandas as pd
import pydeck as pdk
import glob
import os

CSV_DIR = "data/storico"

BBOX_POLYGON = [[
    [10.0, 35.0],
    [15.5, 35.0],
    [15.5, 38.5],
    [10.0, 38.5],
    [10.0, 35.0],
]]

st.set_page_config(page_title="AIS Database GFW", layout="wide")
st.title("AIS — Database Global Fishing Watch")

csv_files = sorted(glob.glob(os.path.join(CSV_DIR, "*.csv")))
if not csv_files:
    st.error(f"Nessun file CSV trovato in: {CSV_DIR}")
    st.stop()

labels = [os.path.basename(f).replace(".csv", "") for f in csv_files]
selected = st.selectbox("Seleziona periodo", labels)
selected_file = csv_files[labels.index(selected)]

df = pd.read_csv(selected_file)
df = df.dropna(subset=["lat", "lon"])

# Aggrega per cella: conteggio navi uniche e somma fishing hours
grid = df.groupby(["lat", "lon"]).agg(
    vessel_count=("mmsi", "nunique"),
    fishing_hours=("fishing_hours", "sum")
).reset_index()

# Soglia fishing hours intense
max_fh = float(grid["fishing_hours"].max())
soglia = st.slider("Soglia fishing hours intense", 0.0, max_fh, max_fh * 0.75, step=0.5)

col1, col2 = st.columns(2)
col1.metric("Celle monitorate", len(grid))
col2.metric("Navi uniche", df["mmsi"].nunique())

# Layer heatmap basato su numero di navi per cella
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=grid,
    get_position=["lon", "lat"],
    get_weight="vessel_count",
    radiusPixels=40,
    opacity=0.8,
)

# Layer tag celle con fishing hours intense
intense = grid[grid["fishing_hours"] >= soglia].copy()
intense["label"] = intense["fishing_hours"].apply(lambda x: f"{x:.1f}h")

tag_layer = pdk.Layer(
    "TextLayer",
    data=intense,
    get_position=["lon", "lat"],
    get_text="label",
    get_size=14,
    get_color=[220, 50, 50, 255],
    get_alignment_baseline="'bottom'",
)

bbox_layer = pdk.Layer(
    "PolygonLayer",
    data=[{"polygon": BBOX_POLYGON}],
    get_polygon="polygon",
    get_fill_color=[0, 0, 255, 20],
    get_line_color=[0, 0, 255, 180],
    get_line_width=3000,
    stroked=True,
    filled=True,
)

view = pdk.ViewState(
    latitude=36.75,
    longitude=12.75,
    zoom=6,
)

st.pydeck_chart(pdk.Deck(
    layers=[bbox_layer, heatmap_layer, tag_layer],
    initial_view_state=view,
    map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
))
