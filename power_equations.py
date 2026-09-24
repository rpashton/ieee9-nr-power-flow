"""
Power Injection Equations
Computes calculated P and Q at every bus from the current V, theta guess:

    P_i = |V_i| * sum_j |V_j| * (G_ij*cos(theta_ij) + B_ij*sin(theta_ij))
    Q_i = |V_i| * sum_j |V_j| * (G_ij*sin(theta_ij) - B_ij*cos(theta_ij))
"""

import numpy as np

def calc_power_injections(V, theta, Ybus):
    n = len(V)
    G = Ybus.real
    B = Ybus.imag

    P_calc = np.zeros(n)
    Q_calc = np.zeros(n)

    for i in range(n):
        for j in range(n):
            theta_ij = theta[i] - theta[j]
            P_calc[i] += V[i] * V[j] * (G[i, j] * np.cos(theta_ij) + B[i, j] * np.sin(theta_ij))
            Q_calc[i] += V[i] * V[j] * (G[i, j] * np.sin(theta_ij) - B[i, j] * np.cos(theta_ij))
    return P_calc, Q_calc

if __name__ == "__main__":
    from ybus import build_ybus
    from ieee9_data import N_BUS

    Ybus = build_ybus()
    V = np.ones(N_BUS)
    theta = np.zeros(N_BUS)

    P_calc, Q_calc = calc_power_injections(V, theta, Ybus)

    for i in range(N_BUS):
        print(f"Bus {i+1}: P = {P_calc[i]:+.4f}   Q = {Q_calc[i]:+.4f}")
