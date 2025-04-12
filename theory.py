# theory.py
import math

def compute_theoretical_distribution(lambda_, mu, m):
    """
    Calcule la distribution théorique et le nombre moyen de clients pour une file M/M/m.
    
    Arguments :
    - lambda_ : taux d'arrivée
    - mu : taux de service par serveur
    - m : nombre de serveurs
    
    Retourne :
    - Pn : liste des probabilités P(n) pour n=0 à max_state
    - P0 : probabilité d'avoir 0 clients
    - L : nombre moyen de clients dans le système
    """
    rho = lambda_ / (m * mu)
    if rho >= 1:
        return [0], 0, float('inf')  # Système instable

    # Calcul de P0 (basé sur la formule du cours)
    sum_terms = sum((lambda_ / mu)**k / math.factorial(k) for k in range(m))
    last_term = (lambda_ / mu)**m / (math.factorial(m) * (1 - rho))
    P0 = 1 / (sum_terms + last_term)

    # Calcul des probabilités Pn
    Pn = []
    max_state = m + 50  # Couvre suffisamment d'états
    for n in range(max_state):
        if n < m:
            prob = ((lambda_ / mu)**n / math.factorial(n)) * P0
        else:
            prob = ((lambda_ / mu)**n / (math.factorial(m) * m**(n - m))) * P0
        Pn.append(prob)

    # Calcul de Lq (nombre moyen dans la file)
    Lq = P0 * ((lambda_ / mu)**m) * rho / (math.factorial(m) * (1 - rho)**2)

    # Calcul de L (nombre moyen dans le système)
    L = Lq + lambda_ / mu

    return Pn, P0, L