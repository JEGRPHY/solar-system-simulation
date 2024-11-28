import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Sidebar controls
speed_factor = st.sidebar.slider("Speed Factor", 0.1, 5.0, 1.0)
scale = st.sidebar.slider("Scale", 1, 100, 10)
zoom = st.sidebar.slider("Zoom Level", 1, 20, 5)

# Time step for planet motion
time = np.linspace(0, 2 * np.pi, 100)

# Planet data (simplified)
planets = [
    {"name": "Mercury", "radius": 0.4, "color": "gray"},
    {"name": "Venus", "radius": 0.7, "color": "orange"},
    {"name": "Earth", "radius": 1.0, "color": "blue"},
    {"name": "Mars", "radius": 1.5, "color": "red"},
    {"name": "Jupiter", "radius": 5.2, "color": "brown"},
    {"name": "Saturn", "radius": 9.5, "color": "gold"},
    {"name": "Uranus", "radius": 19.8, "color": "lightblue"},
    {"name": "Neptune", "radius": 30.1, "color": "darkblue"}
]

# Create the plot
fig = go.Figure()

# Add the Sun
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=10, color='yellow'),
    name='Sun'
))

# Add planets and their orbits
for planet in planets:
    x = planet["radius"] * scale * np.cos(speed_factor * time)
    y = planet["radius"] * scale * np.sin(speed_factor * time)
    z = [0] * len(time)

    # Orbit
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=planet["color"], width=2),
        name=f'{planet["name"]} Orbit'
    ))

    # Planet
    fig.add_trace(go.Scatter3d(
        x=[x[0]], y=[y[0]], z=[0],
        mode='markers',
        marker=dict(size=5, color=planet["color"]),
        name=planet["name"]
    ))

# Adjust layout
fig.update_layout(
    scene=dict(aspectmode="cube"),
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig)
