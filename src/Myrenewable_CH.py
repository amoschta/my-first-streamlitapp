import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

import os
print(os.getcwd())

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

renewable_df_raw = load_data(path="C:\\Users\\Amos\\OneDrive\\Desktop\\Data_science_Bootcamp\\my-first-streamlitapp\\data\\raw\\renewable_power_plants_CH.csv")
renewable_df = deepcopy(renewable_df_raw)

renewable_df.dropna(subset=["lat", "lon"], inplace=True)
st.title("Renewable Power Plants in Switzerland")

#sources=renewable_df["energy_source_level_2"].unique()
#st.dataframe(show)
if  st.checkbox("Show Dataframe"):
    st.subheader("Dataset of renewable power plants in Switzerland")
    st.dataframe(data=renewable_df.head())

sources=["All"]+sorted(renewable_df["energy_source_level_2"].unique())
#print(renewable_df.columns)
#print(f'The renewable energy sources in Switzerland: {renewable_df["energy_source_level_2"].unique()}')
st.subheader("Renewable Energy Sources in Switzerland")
    
selected_source=st.selectbox(f"choose an energy source", options=sources, index=0)
#st.subheader("Select Energy Sources in Switzerland")
#st.write(sources)
if selected_source == "All":
    reduced_df = renewable_df
else:
    reduced_df = renewable_df[renewable_df["energy_source_level_2"]==selected_source]

st.subheader(f" {selected_source} energy Plants in Switzerland")

left_column,midle_column, right_column=st.columns([1,2,1])
show_number_of_plants = left_column.radio("Show Number of Plants", options=["Yes", "No"])
show_total_energy_capacity=right_column.radio("Show Total Energy Capacity", options=["Yes", "No"])
if show_number_of_plants == "Yes":
    number_of_plants = (reduced_df["energy_source_level_2"]==selected_source).count()
    left_column.write(f"Number of {selected_source} plants: {number_of_plants} in Switzerland")
if show_total_energy_capacity == "Yes":
    total_energy_capacity = reduced_df["electrical_capacity"].sum()
    right_column.write(f"Total energy capacity of {selected_source} plants: {total_energy_capacity} MW")
midle_column.write(f"Total produced energy of {selected_source} plants: {reduced_df['production'].sum()} MWh")

#sources_df=renewable_df.groupby("energy_source_level_2").sum(renewable_df["electrical_capacity"]).sum(renewable_df["production"]).reset_index()
sources_df = renewable_df[["energy_source_level_2", "electrical_capacity", "production"]] \
    .groupby("energy_source_level_2").sum().reset_index()
p_fig = px.bar(
    sources_df,
    x="energy_source_level_2",
    y=["electrical_capacity", "production"],
    title="Renewable Energy Production and Capacity in Switzerland",
    labels={"energy_source_level_2":"Energy source","value": "Energy (MWh)", "variable": "Energy Type"},
    #barmode="group"
    width=800,
    height=600
)
st.plotly_chart(p_fig, use_container_width=True)

# Show the map of renewable energy plants in Switzerland
color_map = {
    "Hydro": "blue",
    "Solar": "red",
    "Wind": "green",
    "Biomass": "brown",
}
# Load the canton GeoJSON file
with open("C:\\Users\\Amos\\OneDrive\\Desktop\\Data_science_Bootcamp\\my-first-streamlitapp\\data\\raw\\georef-switzerland-kanton.geojson") as f:
    cantons_geojson = json.load(f)

# Prepare colors for each plant according to energy source
marker_colors = reduced_df["energy_source_level_2"].map(color_map).fillna("gray")

# Create the canton polygons as a background
canton_layer = go.Choroplethmapbox(
    geojson=cantons_geojson,
    locations=[feature["properties"]["kan_name"] for feature in cantons_geojson["features"]if "kan_name" in feature["properties"]],
    z=[1]*len(cantons_geojson["features"]),  # dummy values
    colorscale="Greys",
    showscale=False,
    marker_opacity=0.2,
    marker_line_width=1
)
for feature in cantons_geojson["features"]:
    if "kan_name" not in feature["properties"]:
        print("Missing 'kan_name' in feature:", feature)
# Create your plant markers, colored by energy source
plant_layer = go.Scattermapbox(
    lat=reduced_df["lat"],
    lon=reduced_df["lon"],
    mode="markers",
    marker=go.scattermapbox.Marker(
        size=5*reduced_df["electrical_capacity"]/reduced_df["electrical_capacity"].max(),
        #probably a log scale would be better here
        color=marker_colors
    ),
    text=reduced_df["energy_source_level_2"],
    hoverinfo="text"
)

# Combine both layers in a Figure
map_fig = go.Figure([canton_layer, plant_layer])

map_fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6,
    mapbox_center={"lat": 46.8, "lon": 8.2},
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(map_fig, use_container_width=True)
st.map(reduced_df, zoom=7)  

url="https://open-power-system-data.org/"
"Data Source", url 

print(cantons_geojson["features"][0]["properties"])