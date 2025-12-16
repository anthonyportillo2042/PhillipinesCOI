import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("data/Philippines_COI_Dummy_Data.csv")

# Streamlit Layout
st.set_page_config(page_title="COI Dashboard", layout="wide")
st.title("Philippines COI Dashboard Prototype")

# Sidebar Filters
buckets = df["COI Bucket"].unique()
four_rs = ["Resilience", "Response", "Recovery", "Risk"]

selected_buckets = st.sidebar.multiselect("Select COI Buckets", options=buckets, default=buckets)
selected_4rs = st.sidebar.multiselect("Select 4Rs", options=four_rs, default=four_rs)

filtered_df = df[df["COI Bucket"].isin(selected_buckets) &
                 df["4Rs Impact"].apply(lambda x: any(r in x for r in selected_4rs))]

st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Heatmap
heatmap_data = filtered_df.pivot(index="COI Bucket", columns="Municipality", values="Score")

st.subheader("COI Heatmap")
if heatmap_data.empty:
    st.write("No data to display for selected filters.")
else:
    fig = px.imshow(heatmap_data, text_auto=True, color_continuous_scale="RdYlGn",
                    labels=dict(x="Municipality", y="COI Bucket", color="Score"))
    st.plotly_chart(fig, use_container_width=True)

# Map Overlay Example (Placeholder Coordinates)
st.subheader("Map Overlay Example")
municipality_coords = {
    "Manila": [14.5995, 120.9842],
    "Quezon City": [14.6760, 121.0437],
    "Cebu City": [10.3157, 123.8854],
    "Davao City": [7.1907, 125.4553],
    "Iloilo City": [10.7202, 122.5621]
}
map_df = pd.DataFrame([
    {"Municipality": m, "lat": coords[0], "lon": coords[1], 
     "Score": df[df["Municipality"]==m]["Score"].mean()}
    for m, coords in municipality_coords.items()
])
st.map(map_df)