import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Sidebar controls
speed_factor = st.sidebar.slider("Speed Factor", 0.1, 5.0, 1.0)
scale = st.sidebar.slider("Scale", 1, 100, 10)
zoom = st.sidebar.slider("Zoom Level", 1, 20, 5)

# Time step for motion
t_step = st.sidebar.slider("Time Step (seconds)", 0.01, 0.5, 0.1)

# Planet data (simplified)
planets = [
    {"name": "Mercury", "radius": 0.4, "period": 88, "color": "gray"},
    {"name": "Venus", "radius": 0.7, "period": 225, "color": "orange"},
    {"name": "Earth", "radius": 1.0, "period": 365, "color": "blue"},
    {"name": "Mars", "radius": 1.5, "period": 687, "color": "red"},
    {"name": "Jupiter", "radius": 5.2, "period": 4333, "color": "brown"},
    {"name": "Saturn", "radius": 9.5, "period": 10759, "color": "gold"},
    {"name": "Uranus", "radius": 19.8, "period": 30685, "color": "lightblue"},
    {"name": "Neptune", "radius": 30.1, "period": 60190, "color": "darkblue"}
]

# Initialize time variable
if "time" not in st.session_state:
    st.session_state.time = 0

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
planet_positions = []
for planet in planets:
    # Calculate position of the planet based on time and orbital period
    angle = (st.session_state.time / planet["period"]) * 2 * np.pi * speed_factor
    x = planet["radius"] * scale * np.cos(angle)
    y = planet["radius"] * scale * np.sin(angle)
    z = 0  # Keep the z-axis constant for simplicity

    planet_positions.append((x, y, z))

    # Orbit (a simple circle)
    orbit_t = np.linspace(0, 2 * np.pi, 100)
    orbit_x = planet["radius"] * scale * np.cos(orbit_t)
    orbit_y = planet["radius"] * scale * np.sin(orbit_t)
    orbit_z = [0] * len(orbit_t)

    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines',
        line=dict(color=planet["color"], width=2),
        name=f'{planet["name"]} Orbit'
    ))

    # Planet
    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers',
        marker=dict(size=5, color=planet["color"]),
        name=planet["name"]
    ))

# Adjust layout
fig.update_layout(
    scene=dict(
        aspectmode="cube",
        xaxis=dict(range=[-zoom * scale, zoom * scale]),
        yaxis=dict(range=[-zoom * scale, zoom * scale]),
        zaxis=dict(range=[-zoom * scale, zoom * scale])
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Display the plot
st.plotly_chart(fig)

# Update time for animation
time.sleep(t_step)
st.session_state.time += t_step * 365  # Increment time in days
