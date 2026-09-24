"""
IEEE 9-Bus(WSCC) Test System Data
Source: MATPOWER case9.m standard reference. Base MVA = 100.
"""

BASE_MVA = 100.0

# bus_id, type, Pd(MW), Qd(MVAr), Vsp(pu), Pg(MW)
BUS_DATA = [
    (1, "slack", 0.0, 0.0, 1.0, 0.0),
    (2, "PV",    0.0, 0.0, 1.0, 163.0),
    (3, "PV",    0.0, 0.0, 1.0, 85.0),
    (4, "PQ",    0.0, 0.0, 1.0, 0.0),
    (5, "PQ",    90.0, 30.0, 1.0, 0.0),
    (6, "PQ",    0.0,   0.0,   1.0, 0.0),
    (7, "PQ",    100.0, 35.0,  1.0, 0.0),
    (8, "PQ",    0.0,   0.0,   1.0, 0.0),
    (9, "PQ",    125.0, 50.0,  1.0, 0.0),
]

# from, to, R(pu), X(pu), B_totl (pu, full line charging susceptance)
LINE_DATA = [
    (4, 5, 0.0170, 0.0920, 0.1580),
    (5, 6, 0.0390, 0.1700, 0.3580),
    (6, 7, 0.0119, 0.1008, 0.2090),
    (7, 8, 0.0085, 0.0720, 0.1490),
    (8, 9, 0.0320, 0.1610, 0.3060),
    (9, 4, 0.0100, 0.0850, 0.1760),
]

# from, to, X(pu) | transformers: R=0, no charging susceptance
TRANSFORMER_DATA = [
    (1, 4, 0.0576),
    (3, 6, 0.0586),
    (8, 2, 0.0625),
]

N_BUS = len(BUS_DATA)

# Newton-Raphson impplementation (pandapower), used to check our solver

REFERENCE_SOLUTION = {
    1: (1.000000, 0.000000),
    2: (1.000000, 9.668741),
    3: (1.000000, 4.771073),
    4: (0.987007, -2.406644),
    5: (0.975472, -4.017264),
    6: (1.003375, 1.925602),
    7: (0.985645, 0.621545),
    8: (0.996185, 3.799120),
    9: (0.957621, -4.349934),
}