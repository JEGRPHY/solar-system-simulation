import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Solar System Simulation",
    page_icon="🌌",
    layout="wide"
)

# Title and Description
st.title("🌌 Solar System Simulation")
st.markdown("""
Welcome to the **interactive solar system simulation**! 🌍✨  
Here, you can visualize the motion of planets around the Sun and customize the simulation to your liking.  
Use the controls on the left to:
- Adjust **speed**, **scale**, and **zoom**.
- Add **custom planets** with unique properties.
- Watch planets orbit the Sun in real time!  
""")

# Sidebar layout
st.sidebar.title("Simulation Controls")

# Section: Planetary Motion
st.sidebar.header("🌍 Planetary Motion")
speed_factor = st.sidebar.slider("Speed Factor", 0.1, 5.0, 1.0, help="Adjust how fast the planets move.")
scale = st.sidebar.slider("Scale", 1, 100, 10, help="Change the size of orbits.")
zoom = st.sidebar.slider("Zoom Level", 1, 20, 5, help="Zoom in or out for better viewing.")
t_step = st.sidebar.slider("Time Step (seconds)", 0.01, 0.5, 0.1, help="Control the animation speed.")

# Section: Add Custom Planet
st.sidebar.header("🪐 Add a Custom Planet")
custom_name = st.sidebar.text_input("Planet Name", value="New Planet")
custom_radius = st.sidebar.slider("Orbit Radius (AU)", 0.5, 40.0, 10.0, help="Set the distance of the planet from the Sun.")
custom_period = st.sidebar.slider("Orbital Period (days)", 1, 10000, 365, help="Set the time it takes for the planet to complete one orbit.")
custom_color = st.sidebar.color_picker("Planet Color", value="#FFFFFF")
add_planet = st.sidebar.button("Add Planet")

# Save custom planets in session state
if "custom_planets" not in st.session_state:
    st.session_state.custom_planets = []

if add_planet:
    st.session_state.custom_planets.append({
        "name": custom_name,
        "radius": custom_radius,
        "period": custom_period,
        "color": custom_color
    })
    st.sidebar.success(f"Added {custom_name} to the solar system!")

# Section: Reset Button
st.sidebar.header("🔄 Reset")
if st.sidebar.button("Reset Simulation"):
    st.session_state.time = 0
    st.session_state.custom_planets = []
    st.sidebar.info("Simulation reset successfully!")

# Track simulation time
if "time" not in st.session_state:
    st.session_state.time = 0

# Default planets
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

# Create 3D plot
fig = go.Figure()

# Add the Sun
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=20, color='yellow'),
    name='Sun'
))

# Add planets and their orbits
for planet in planets:
    angle = (st.session_state.time / planet["period"]) * 2 * np.pi * speed_factor
    x = planet["radius"] * scale * np.cos(angle)
    y = planet["radius"] * scale * np.sin(angle)
    z = 0  # Keep in a flat plane

    orbit_t = np.linspace(0, 2 * np.pi, 100)
    orbit_x = planet["radius"] * scale * np.cos(orbit_t)
    orbit_y = planet["radius"] * scale * np.sin(orbit_t)
    orbit_z = [0] * len(orbit_t)

    # Add orbit
    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines',
        line=dict(color=planet["color"], width=2),
        name=f"{planet['name']} Orbit"
    ))

    # Add planet
    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers',
        marker=dict(size=8, color=planet["color"]),
        name=planet["name"]
    ))

# Adjust layout for 3D visualization
fig.update_layout(
    scene=dict(
        aspectmode="cube",
        xaxis=dict(range=[-zoom * scale, zoom * scale]),
        yaxis=dict(range=[-zoom * scale, zoom * scale]),
        zaxis=dict(range=[-zoom * scale, zoom * scale])
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(
        title="Legend",
        font=dict(size=10),
        itemsizing="constant"
    )
)

# Display 3D plot
st.plotly_chart(fig)

# Update simulation time
time.sleep(t_step)
st.session_state.time += t_step * 365  # Increment time in days
