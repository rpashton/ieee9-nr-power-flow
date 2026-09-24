"""
Jacobian Builder

Builds the Newton-Raphson Jacobian: 4 blocks (J1..J4), each with
off-diagonal (trig-based) and diagonal (shortcut-formula) entries.
"""

import numpy as np


def build_jacobian(V, theta, Ybus, P_calc, Q_calc, non_slack_idx, pq_idx):
    G = Ybus.real
    B = Ybus.imag

    n_theta = len(non_slack_idx)
    n_v = len(pq_idx)
    J = np.zeros((n_theta + n_v, n_theta + n_v))

    # J1 = dP/dtheta 
    for a, i in enumerate(non_slack_idx):
        for b, j in enumerate(non_slack_idx):
            if i == j:
                J[a, b] = -Q_calc[i] - B[i, i] * V[i] ** 2
            else:
                theta_ij = theta[i] - theta[j]
                J[a, b] = V[i] * V[j] * (G[i, j] * np.sin(theta_ij) - B[i, j] * np.cos(theta_ij))

        #  J2 = dP/d|V| 
    for a, i in enumerate(non_slack_idx):
        for b, j in enumerate(pq_idx):
            if i == j:
                J[a, n_theta + b] = P_calc[i] / V[i] + G[i, i] * V[i]
            else:
                theta_ij = theta[i] - theta[j]
                J[a, n_theta + b] = V[i] * (G[i, j] * np.cos(theta_ij) + B[i, j] * np.sin(theta_ij))

        #  J3 = dQ/dtheta 
    for a, i in enumerate(pq_idx):
        for b, j in enumerate(non_slack_idx):
            if i == j:
                J[n_theta + a, b] = P_calc[i] - G[i, i] * V[i] ** 2
            else:
                theta_ij = theta[i] - theta[j]
                J[n_theta + a, b] = -V[i] * V[j] * (G[i, j] * np.cos(theta_ij) + B[i, j] * np.sin(theta_ij))

    #  J4 = dQ/d|V| 
    for a, i in enumerate(pq_idx):
        for b, j in enumerate(pq_idx):
            if i == j:
                J[n_theta + a, n_theta + b] = Q_calc[i] / V[i] - B[i, i] * V[i]
            else:
                theta_ij = theta[i] - theta[j]
                J[n_theta + a, n_theta + b] = V[i] * (G[i, j] * np.sin(theta_ij) - B[i, j] * np.cos(theta_ij))

    return J