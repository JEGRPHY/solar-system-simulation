import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Sidebar controls
speed_factor = st.sidebar.slider("Speed Factor", 0.1, 5.0, 1.0)
scale = st.sidebar.slider("Scale", 1, 100, 10)
zoom = st.sidebar.slider("Zoom Level", 1, 20, 5)

# Planet positions (update dynamically)
t = np.linspace(0, 2 * np.pi, 100)
x = scale * np.cos(t)
y = scale * np.sin(t)

# Create 3D plot
fig = go.Figure()

# Add Sun
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0],
                           mode='markers',
                           marker=dict(size=10, color='yellow'),
                           name='Sun'))

# Add a planet
fig.add_trace(go.Scatter3d(x=x, y=y, z=[0]*len(t),
                           mode='lines',
                           line=dict(color='blue'),
                           name='Earth Orbit'))

# Adjust view
fig.update_layout(scene=dict(aspectmode='cube'),
                  margin=dict(l=0, r=0, b=0, t=0))

st.plotly_chart(fig)

