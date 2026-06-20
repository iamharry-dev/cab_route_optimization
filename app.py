import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.optimizer import CabRouteOptimizer
from src.utils import generate_savings_report

st.set_page_config(page_title="Cab Route Optimization", layout="wide")

st.title("🚕 Cab Route Optimization")
st.markdown("*Find the shortest path — save time and fuel*")

@st.cache_resource
def load_optimizer():
    return CabRouteOptimizer()

optimizer = load_optimizer()

st.sidebar.header("Select Route")
locations = list(optimizer.G.nodes())

pickup = st.sidebar.selectbox("Pickup Location", locations, index=0)
dropoff = st.sidebar.selectbox("Dropoff Location", locations, index=5)

if st.sidebar.button("🚀 Optimize Route"):
    result = optimizer.optimize_route(pickup, dropoff)
    
    if result:
        st.success("Route Optimized!")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Distance", f"{result['distance_km']} km")
        col2.metric("Trip Time", f"{result['trip_time_min']} min")
        col3.metric("Fuel Cost", f"₹{result['fuel_cost']}")
        col4.metric("Stops", f"{result['path_length']}")
        
        st.subheader("🗺️ Optimized Route")
        st.info(f"**{result['route']}**")
        
        path_nodes = result['route'].split(' → ')
        lats = [optimizer.city_graph.positions[n][0] for n in path_nodes]
        lons = [optimizer.city_graph.positions[n][1] for n in path_nodes]
        
        fig = go.Figure()
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons,
            mode='lines+markers+text',
            text=path_nodes,
            textposition='top center',
            line=dict(width=3, color='blue'),
            marker=dict(size=10, color='red')
        ))
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=13.0, lon=80.25), zoom=11),
            height=500, margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📊 Batch Optimization")

sample_routes = pd.DataFrame({
    'pickup': ['T. Nagar', 'Adyar', 'Anna Nagar', 'Velachery', 'Guindy'],
    'dropoff': ['Airport', 'OMR', 'Sholinganallur', 'ECR', 'Tambaram']
})

optimized_df = optimizer.batch_optimize(sample_routes)
st.dataframe(optimized_df)

report = generate_savings_report(optimized_df)
st.code(report, language=None)

st.divider()

st.subheader("🔥 Demand Heatmap by Hour")
hour = st.slider("Select Hour", 0, 23, 8)
demand_df = optimizer.get_demand_heatmap_data()
hourly_demand = demand_df[demand_df['hour'] == hour]

fig = px.scatter_mapbox(
    hourly_demand, lat='lat', lon='lon', size='demand',
    color='demand', color_continuous_scale='Hot',
    size_max=20, zoom=11
)
fig.update_layout(mapbox_style="open-street-map", height=500)
st.plotly_chart(fig, use_container_width=True)
