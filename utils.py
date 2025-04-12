import plotly.graph_objects as go
import streamlit as st

def plot_distributions(empirical, theoretical):
    """
    Trace la comparaison entre les distributions empirique et théorique avec Plotly.
    """
    max_state = max(len(empirical), len(theoretical))
    states = list(range(max_state))
    emp_vals = [empirical[i] if i < len(empirical) else 0 for i in states]
    theo_vals = [theoretical[i] if i < len(theoretical) else 0 for i in states]


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=states, y=theo_vals, mode='lines+markers', name='Théorique', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=states, y=emp_vals, mode='lines+markers', name='Empirique', line=dict(color='red', dash='dash')))
    
    fig.update_layout(
        title="Comparaison des distributions",
        xaxis_title="Nombre de clients dans le système",
        yaxis_title="Probabilité",
        hovermode="x unified",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)