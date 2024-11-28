import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Solar System with JEGR",
    page_icon="🌌",
    layout="wide"
)

# Title and Introduction
st.title("🌌Solar System with JEGR")
st.markdown("""
Explore the **physics behind the solar system**! 🪐  
This simulation models the motion of planets around the Sun using principles of **orbital mechanics**.  
Key concepts:
- **Newton's Law of Gravitation** governs the forces between celestial bodies.
- **Kepler's Laws** determine orbital paths and periods.
""")

# Sidebar Layout
st.sidebar.title("Simulation Controls")
st.sidebar.header("🌍 Planetary Motion")
speed_factor = st.sidebar.slider("Speed Factor", 0.1, 5.0, 1.0, help="Adjust the relative speed of planet orbits.")
scale = st.sidebar.slider("Scale", 1, 100, 10, help="Adjust the scale of the solar system.")
zoom = st.sidebar.slider("Zoom Level", 1, 20, 5, help="Zoom in or out of the visualization.")
t_step = st.sidebar.slider("Time Step (seconds)", 0.01, 0.5, 0.1, help="Control the speed of the animation.")

# Physics Information
st.sidebar.header("🔬 Physics Information")
selected_planet = st.sidebar.selectbox("Select Planet", ["Sun"] + ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
show_physics = st.sidebar.checkbox("Show Physics Data", value=True)

# Reset Button
if st.sidebar.button("Reset Simulation"):
    st.session_state.time = 0
    st.sidebar.info("Simulation reset successfully!")

# Initialize Session State
if "time" not in st.session_state:
    st.session_state.time = 0

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
solar_mass = 1.989e30  # Mass of the Sun (kg)

# Planet Data
planets = [
    {"name": "Mercury", "radius": 0.4, "mass": 3.3e23, "period": 88, "color": "gray"},
    {"name": "Venus", "radius": 0.7, "mass": 4.87e24, "period": 225, "color": "orange"},
    {"name": "Earth", "radius": 1.0, "mass": 5.97e24, "period": 365, "color": "blue"},
    {"name": "Mars", "radius": 1.5, "mass": 6.42e23, "period": 687, "color": "red"},
    {"name": "Jupiter", "radius": 5.2, "mass": 1.9e27, "period": 4333, "color": "brown"},
    {"name": "Saturn", "radius": 9.5, "mass": 5.68e26, "period": 10759, "color": "gold"},
    {"name": "Uranus", "radius": 19.8, "mass": 8.68e25, "period": 30685, "color": "lightblue"},
    {"name": "Neptune", "radius": 30.1, "mass": 1.02e26, "period": 60190, "color": "darkblue"}
]

# Physics Data for Selected Planet
if selected_planet != "Sun":
    planet_data = next(p for p in planets if p["name"] == selected_planet)
    distance_m = planet_data["radius"] * 1.496e11  # AU to meters
    orbital_velocity = np.sqrt(G * solar_mass / distance_m)  # Orbital velocity (m/s)
    st.sidebar.markdown(f"""
    **{selected_planet} Physics**:
    - Orbital Radius: {planet_data["radius"]} AU
    - Orbital Velocity: {orbital_velocity / 1000:.2f} km/s
    - Orbital Period: {planet_data["period"]} days
    """)
else:
    st.sidebar.markdown("The Sun is the center of the solar system, exerting gravitational force on all planets.")

# Create 3D Plot
fig = go.Figure()

# Add the Sun
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(size=20, color='yellow'),
    name='Sun'
))

# Add planets and orbits
for planet in planets:
    angle = (st.session_state.time / planet["period"]) * 2 * np.pi * speed_factor
    x = planet["radius"] * scale * np.cos(angle)
    y = planet["radius"] * scale * np.sin(angle)
    z = 0

    orbit_t = np.linspace(0, 2 * np.pi, 100)
    orbit_x = planet["radius"] * scale * np.cos(orbit_t)
    orbit_y = planet["radius"] * scale * np.sin(orbit_t)
    orbit_z = [0] * len(orbit_t)

    # Orbit path
    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines',
        line=dict(color=planet["color"], width=2),
        name=f"{planet['name']} Orbit"
    ))

    # Planet marker
    fig.add_trace(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers',
        marker=dict(size=8, color=planet["color"]),
        name=planet["name"]
    ))

# Add grid and layout adjustments
fig.update_layout(
    scene=dict(
        xaxis=dict(title="X (AU)", range=[-zoom * scale, zoom * scale]),
        yaxis=dict(title="Y (AU)", range=[-zoom * scale, zoom * scale]),
        zaxis=dict(title="Z (AU)", range=[-zoom * scale, zoom * scale]),
        aspectmode="cube"
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    title="Solar System Visualization"
)

# Display the 3D plot
st.plotly_chart(fig)

# Update time for animation
time.sleep(t_step)
st.session_state.time += t_step * 365
