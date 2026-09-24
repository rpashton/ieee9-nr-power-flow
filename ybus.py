"""
Ybus Builder
Constructs the bus admittance matrix from line and transformer data.

For a branch between bus i and bus j with series admittance y = 1/(R+jX)
and total shunt charging susceptance B:

    Y[i][i] += y + jB/2
    Y[j][j] += y + jB/2
    Y[i][j] -= y
    Y[j][i] -= y
"""

import numpy as np

from ieee9_data import N_BUS, LINE_DATA, TRANSFORMER_DATA

def build_ybus(n_bus=N_BUS, lines=LINE_DATA, transformers=TRANSFORMER_DATA):

    Ybus = np.zeros((n_bus,n_bus), dtype=complex)

    for from_bus, to_bus, R, X, B in lines:
        i = from_bus - 1
        j = to_bus - 1

        y_series = 1.0 / complex(R,X)
        y_shunt = 1j * B / 2.0

        Ybus[i, i] += y_series + y_shunt
        Ybus[j, j] += y_series + y_shunt
        Ybus[i, j] -= y_series
        Ybus[j, i] -= y_series

    for from_bus, to_bus, X in transformers:
        i = from_bus - 1
        j = to_bus - 1

        y_series = 1.0 / complex(0.0, X)

        Ybus[i, i] += y_series
        Ybus[j, j] += y_series
        Ybus[i, j] -= y_series
        Ybus[j, i] -= y_series


    return Ybus

if __name__ == "__main__":

    Ybus = build_ybus()
    np.set_printoptions(precision=3, suppress=True, linewidth=160)
    print(Ybus)