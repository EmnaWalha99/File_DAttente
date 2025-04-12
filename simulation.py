import numpy as np
import streamlit as st

def simulate_queue(lambda_, mu, m, num_transitions=10000):
    """
    Simule une file d'attente M/M/m avec temps de séjour exponentiel.
    
    Arguments :
    - lambda_ : taux d'arrivée
    - mu : taux de service par serveur
    - m : nombre de serveurs
    - num_transitions : nombre total de transitions
    
    Retourne :
    - distribution_empirique : liste des probabilités par état
    - moyenne_clients : moyenne des clients sur les 5000 dernières transitions
    """
    if lambda_ / (m * mu) >= 1:
        st.warning("Système instable (rho ≥ 1). Les résultats peuvent être non fiables.")

    state = 0  # État initial : aucun client
    history = []

    for _ in range(num_transitions):
        # Taux totaux
        arrival_rate = lambda_
        service_rate = min(state, m) * mu  # Service limité par le nombre de serveurs occupés
        total_rate = arrival_rate + service_rate

        # Temps de séjour (loi exponentielle)
        sojourn_time = np.random.exponential(1 / total_rate) if total_rate > 0 else float('inf')

        # Probabilité d'une arrivée
        prob_arrival = arrival_rate / total_rate if total_rate > 0 else 1.0

        # Transition
        if np.random.rand() < prob_arrival:
            state += 1  # Arrivée
        else:
            state = max(0, state - 1)  # Départ

        history.append(state)

    # Analyse des 5000 dernières transitions (régime asymptotique)
    recent_states = history[-5000:]
    max_state = max(recent_states) + 1
    distribution_empirique = [0] * max_state

    for s in recent_states:
        if s < max_state:
            distribution_empirique[s] += 1

    total = len(recent_states)
    distribution_empirique = [count / total for count in distribution_empirique]
    moyenne_clients = np.mean(recent_states)

    return distribution_empirique, moyenne_clients