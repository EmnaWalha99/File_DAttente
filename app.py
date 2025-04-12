import streamlit as st
import matplotlib.pyplot as plt
from theory import compute_theoretical_distribution
from simulation import simulate_queue
from utils import plot_distributions

st.set_page_config(page_title="Simulation File M/M/m", layout="wide")

st.title("Simulation d'une File d'Attente M/M/m")

col_params, col_results, col_explanations = st.columns([1, 2, 1])

with col_params:
    st.header("Paramètres")
    lam = st.number_input("Taux d'arrivée (λ)", min_value=0.1, value=4.0, step=0.1, key="lambda")
    mu = st.number_input("Taux de service (μ)", min_value=0.1, value=2.0, step=0.1, key="mu")
    m = st.slider("Nombre de serveurs (m)", min_value=1, max_value=10, value=3, key="servers")
    num_transitions = st.number_input("Nombre de transitions", min_value=1000, max_value=50000, value=10000, step=1000, key="transitions")

    rho = lam / (m * mu)
    if rho >= 1:
        st.error("⚠️ Système instable (ρ ≥ 1).")
    else:
        st.info(f"Taux d'occupation (ρ) : {rho:.2f}")

    if st.button("Lancer la Simulation"):
        with st.spinner("Simulation en cours..."):
            theoretical_dist, P0, theoretical_L = compute_theoretical_distribution(lam, mu, m)
            empirical_dist, empirical_L = simulate_queue(lam, mu, m, num_transitions)
            st.session_state.results = {
                "theoretical_dist": theoretical_dist,
                "empirical_dist": empirical_dist,
                "theoretical_L": theoretical_L,
                "empirical_L": empirical_L,
                "rho": rho
            }
            st.success("Simulation terminée !")

# Colonne 2 : Résultats
with col_results:
    st.header("Résultats")
    if "results" in st.session_state:
        results = st.session_state.results
        
        # Métriques clés
        st.subheader("Métriques Clés")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Taux d'occupation (ρ)", f"{results['rho']:.2f}")
        col_m2.metric("Nombre de clients présents (N, théorique)", f"{results['theoretical_L']:.2f}")
        col_m3.metric("Nombre de clients présents (N, empirique)", f"{results['empirical_L']:.2f}")
        
        # Graphique
        st.subheader("Distribution de N (théorique vs empirique)")
        plot_distributions(results["empirical_dist"], results["theoretical_dist"])
    else:
        st.info("Lancez une simulation pour voir les résultats.")

# Colonne 3 : Explications
with col_explanations:
    st.header("Explications")
    with st.expander("Formules", expanded=False):
        st.markdown("""
        - **Taux d'occupation** : ρ = λ / (m × μ)
        - **P₀ (N = 0)** : P₀ = [∑(k=0 à m-1) ((λ/μ)ᵏ / k!) + (λ/μ)ᵐ / (m! × (1 - ρ))]⁻¹
        - **File (Lq)** : Lq = P₀ × (λ/μ)ᵐ × ρ / (m! × (1 - ρ)²)
        - **Nombre de clients (N)** : E[N] = Lq + λ/μ
        """)
    
    with st.expander("Détails", expanded=False):
        st.markdown("""
        - **Modèle** : File M/M/m (arrivées et services exponentiels).
        - **Simulation** : 10 000 transitions, analyse des 5 000 dernières.
        - **N** : Nombre de clients présents dans le système.
        - **Stabilité** : Nécessite ρ < 1.
        """)

# Footer
st.markdown("---")
st.caption("Simulation M/M/m.")