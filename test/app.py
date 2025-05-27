import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)

st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

# st.table(data=mpg_df)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset")
    st.dataframe(data=mpg_df)

# left_column, right_column = st.columns(2)
# left_column.checkbox("Left")
# right_column.checkbox("Right")
#a,b,c,d = st.columns([3,1,2,1])
# 3+1+2+1 = 7
# a column: 3/7 of the whole range
#a.checkbox("a")
#b.checkbox("b")
#c.checkbox("c")
#d.checkbox("d")

left_column, middle_column, right_column = st.columns([3,1,1])
years = ["All"] + sorted(pd.unique(mpg_df["year"]))
year = left_column.selectbox("Choose a year", years)

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"]==year]

show_means = middle_column.radio(label = "Show Class Means", options = ["Yes", "No"]) #for horizontal: horizontal = True
means = reduced_df.groupby("class").mean(numeric_only=True)

plot_types = ["matplotlib", "plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

p_fig = px.scatter(
    reduced_df,
    x = "displ",
    y = "hwy",
    range_x = [1,8],
    range_y = [10,50],
    width = 750,
    height = 600,
    labels = {"displ" : "Displacement (Liters)",
              "hwy": "MPG"},
    title = "Engine Size vs Highway Fuel Mileage"
)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means["displ"], y=means["hwy"], mode = "markers"))
    p_fig.update_layout(showlegend = False)


m_fig, ax = plt.subplots(figsize=(10,8))
ax.scatter(reduced_df["displ"], reduced_df["hwy"], alpha = 0.7)
ax.set_title("Engine Size vs Highway Fuel Mileage")
ax.set_xlabel("Displacement (Liters)")
ax.set_ylabel("MPG")

if show_means == "Yes":
    ax.scatter(means["displ"],means["hwy"], alpha = 0.7, color = "red", label = "Class Means")

# st.plotly_chart(p_fig)

if plot_type == "matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source", url)
# "This works too", url

st.subheader("Streamlit Map")
ds_geo = px.data.carshare()
ds_geo["lat"] = ds_geo["centroid_lat"]
ds_geo["lon"] = ds_geo["centroid_lon"]

st.dataframe(ds_geo.head())

st.map(ds_geo)