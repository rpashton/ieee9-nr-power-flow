"""
Line Flow and Loss Calculations

This computes real/reactive power flow on each branch, and total losses.

For a branch from bus i to bus j:
    S_ij = Vi * conj(Yii_branch * Vi + Yij_branch * Vj)
Using the branch's own admittance (not the full Ybus row), so we
rebuild each branch's individual y_series/y_shunt here.
"""

import numpy as np
from newton_raphson import solve_power_flow
from ieee9_data import LINE_DATA, TRANSFORMER_DATA, BASE_MVA


def calc_line_flows():
    result = solve_power_flow(verbose=False)
    V, theta = result["V"], result["theta"]
    Vphasor = V * np.exp(1j * theta)

    print(f"{'From':>5} {'To':>5} {'P_flow(MW)':>12} {'Q_flow(MVAr)':>13} {'Loss(MW)':>10}")

    total_loss_mw = 0.0

    for from_bus, to_bus, R, X, B in LINE_DATA:
        i, j = from_bus - 1, to_bus - 1
        y_series = 1.0 / complex(R, X)
        y_shunt = 1j * B / 2.0

        I_ij = (Vphasor[i] - Vphasor[j]) * y_series + Vphasor[i] * y_shunt
        S_ij = Vphasor[i] * np.conj(I_ij)

        I_ji = (Vphasor[j] - Vphasor[i]) * y_series + Vphasor[j] * y_shunt
        S_ji = Vphasor[j] * np.conj(I_ji)

        loss_mw = (S_ij.real + S_ji.real) * BASE_MVA
        total_loss_mw += loss_mw

        print(f"{from_bus:>5} {to_bus:>5} {S_ij.real*BASE_MVA:>12.3f} "
              f"{S_ij.imag*BASE_MVA:>13.3f} {loss_mw:>10.4f}")

    for from_bus, to_bus, X in TRANSFORMER_DATA:
        i, j = from_bus - 1, to_bus - 1
        y_series = 1.0 / complex(0.0, X)

        I_ij = (Vphasor[i] - Vphasor[j]) * y_series
        S_ij = Vphasor[i] * np.conj(I_ij)

        I_ji = (Vphasor[j] - Vphasor[i]) * y_series
        S_ji = Vphasor[j] * np.conj(I_ji)

        loss_mw = (S_ij.real + S_ji.real) * BASE_MVA
        total_loss_mw += loss_mw

        print(f"{from_bus:>5} {to_bus:>5} {S_ij.real*BASE_MVA:>12.3f} "
              f"{S_ij.imag*BASE_MVA:>13.3f} {loss_mw:>10.4f}")

    print(f"\nTotal system real power losses: {total_loss_mw:.4f} MW")


if __name__ == "__main__":
    calc_line_flows()