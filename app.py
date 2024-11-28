import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Sidebar controls
st.sidebar.title("Solar System Controls")
speed_factor = st.sidebar.slider("Speed Factor", 0.1, 5.0, 1.0)
scale = st.sidebar.slider("Scale", 1, 100, 10)
zoom = st.sidebar.slider("Zoom Level", 1, 20, 5)
t_step = st.sidebar.slider("Time Step (seconds)", 0.01, 0.5, 0.1)

# Custom Planet Feature
st.sidebar.header("Add Custom Planet")
custom_name = st.sidebar.text_input("Planet Name", value="New Planet")
custom_radius = st.sidebar.slider("Orbit Radius", 0.5, 40.0, 10.0)
custom_period = st.sidebar.slider("Orbital Period (days)", 1, 10000, 365)
custom_color = st.sidebar.color_picker("Planet Color", value="#FFFFFF")
add_planet = st.sidebar.button("Add Planet")

# Store added planets in session state
if "custom_planets" not in st.session_state:
    st.session_state.custom_planets = []

if add_planet:
    st.session_state.custom_planets.append({
        "name": custom_name,
        "radius": custom_radius,
        "period": custom_period,
        "color": custom_color
    })

# Time tracking
if "time" not in st.session_state:
    st.session_state.time = 0

# Planet data
default_planets = [
    {"name": "Mercury", "radius": 0.4, "period": 88, "color": "gray"},
    {"name": "Venus", "radius": 0.7, "period": 225, "color": "orange"},
    {"name": "Earth", "radius": 1.0, "period": 365, "color": "blue"},
    {"name": "Mars", "radius": 1.5, "period": 687, "color": "red"},
    {"name": "Jupiter", "radius": 5.2, "period": 4333, "color": "brown"},
    {"name": "Saturn", "radius": 9.5, "period": 10759, "color": "gold"},
    {"name": "Uranus", "radius": 19.8, "period": 30685, "color": "lightblue"},
    {"name": "Neptune", "radius": 30.1, "period": 60190, "color": "darkblue"}
]

# Combine default and custom planets
planets = default_planets + st.session_state.custom_planets

# Create the 3D plot
fig = go.Figure()

# Add the Sun
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=15, color='yellow'),
    name='Sun'
))

# Add planets and their orbits
for planet in planets:
    # Calculate the position of the planet based on time and orbital period
    angle = (st.session_state.time / planet["period"]) * 2 * np.pi * speed_factor
    x = planet["radius"] * scale * np.cos(angle)
    y = planet["radius"] * scale * np.sin(angle)
    z = 0  # Flat 2D plane for simplicity

    # Orbit (circle)
    orbit_t = np.linspace(0, 2 * np.pi, 100)
    orbit_x = planet["radius"] * scale * np.cos(orbit_t)
    orbit_y = planet["radius"] * scale * np.sin(orbit_t)
    orbit_z = [0] * len(orbit_t)

    # Add orbit path
    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines',
        line=dict(color=planet["color"], width=2),
        name=f'{planet["name"]} Orbit'
    ))

    # Add planet
    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers',
        marker=dict(size=8, color=planet["color"]),
        name=planet["name"]
    ))

# Adjust layout for the 3D view
fig.update_layout(
    scene=dict(
        aspectmode="cube",
        xaxis=dict(range=[-zoom * scale, zoom * scale]),
        yaxis=dict(range=[-zoom * scale, zoom * scale]),
        zaxis=dict(range=[-zoom * scale, zoom * scale])
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Display the 3D plot
st.plotly_chart(fig)

# Increment time for animation
time.sleep(t_step)
st.session_state.time += t_step * 365  # Simulate time passing in days
