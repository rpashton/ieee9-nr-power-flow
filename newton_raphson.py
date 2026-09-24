"""
Newton-Raphson Power Flow Solver
Ties together Ybus, power equations, and the Jacobian into the full
iterative solve.
"""

import numpy as np
from ybus import build_ybus
from power_equations import calc_power_injections
from jacobian import build_jacobian
from ieee9_data import BUS_DATA, BASE_MVA, N_BUS


def solve_power_flow(tol=1e-6, max_iter=20, verbose=True):
    Ybus = build_ybus()

    bus_type = {}
    V = np.ones(N_BUS)
    theta = np.zeros(N_BUS)
    P_spec = np.zeros(N_BUS)
    Q_spec = np.zeros(N_BUS)

    slack_idx = None
    pv_idx = []
    pq_idx = []

    for bus_id, btype, Pd, Qd, Vsp, Pg in BUS_DATA:
        i = bus_id - 1
        bus_type[i] = btype
        P_spec[i] = (Pg - Pd) / BASE_MVA
        Q_spec[i] = (-Qd) / BASE_MVA

        if btype == "slack":
            slack_idx = i
            V[i] = Vsp
            theta[i] = 0.0
        elif btype == "PV":
            pv_idx.append(i)
            V[i] = Vsp
        else:
            pq_idx.append(i)

    non_slack_idx = sorted(pv_idx + pq_idx)
    pq_idx = sorted(pq_idx)

    history = []

    if verbose:
        print(f"Slack bus: {slack_idx + 1}   PV buses: {[i+1 for i in pv_idx]}   "
              f"PQ buses: {[i+1 for i in pq_idx]}")

    converged = False
    for iteration in range(1, max_iter + 1):
        P_calc, Q_calc = calc_power_injections(V, theta, Ybus)

        dP = P_spec[non_slack_idx] - P_calc[non_slack_idx]
        dQ = Q_spec[pq_idx] - Q_calc[pq_idx]
        mismatch = np.concatenate([dP, dQ])
        max_mismatch = np.max(np.abs(mismatch))
        history.append(max_mismatch)

        if verbose:
            print(f"Iteration {iteration}: max mismatch = {max_mismatch:.8f} pu")

        if max_mismatch < tol:
            converged = True
            if verbose:
                print(f"\nConverged in {iteration} iterations.\n")
            break

        J = build_jacobian(V, theta, Ybus, P_calc, Q_calc, non_slack_idx, pq_idx)
        dx = np.linalg.solve(J, mismatch)

        n_theta = len(non_slack_idx)
        d_theta = dx[:n_theta]
        d_V = dx[n_theta:]

        for k, i in enumerate(non_slack_idx):
            theta[i] += d_theta[k]
        for k, i in enumerate(pq_idx):
            V[i] += d_V[k]

    if not converged and verbose:
        print(f"\nWARNING: did not converge within {max_iter} iterations.\n")

    return {
        "V": V, "theta": theta, "converged": converged,
        "iterations": len(history), "history": history,
    }


if __name__ == "__main__":
    result = solve_power_flow()

    print("Final bus voltages:")
    print(f"{'Bus':>4} {'|V| (pu)':>10} {'theta (deg)':>12}")
    for i in range(N_BUS):
        print(f"{i+1:>4} {result['V'][i]:>10.4f} {np.degrees(result['theta'][i]):>12.3f}")