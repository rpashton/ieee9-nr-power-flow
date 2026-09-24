"""
Validation: compare our solver's output against the reference solution.
"""

import numpy as np
from newton_raphson import solve_power_flow
from ieee9_data import REFERENCE_SOLUTION, N_BUS


def validate():
    result = solve_power_flow(verbose=False)
    V = result["V"]
    theta_deg = np.degrees(result["theta"])

    print(f"{'Bus':>4} {'V_ours':>10} {'V_ref':>10} {'V err %':>10} "
          f"{'ang_ours':>10} {'ang_ref':>10} {'ang err':>10}")

    max_v_err = 0
    for i in range(N_BUS):
        v_ref, a_ref = REFERENCE_SOLUTION[i + 1]
        v_err_pct = abs(V[i] - v_ref) / v_ref * 100
        a_err = abs(theta_deg[i] - a_ref)
        max_v_err = max(max_v_err, v_err_pct)

        print(f"{i+1:>4} {V[i]:>10.5f} {v_ref:>10.5f} {v_err_pct:>9.5f}% "
              f"{theta_deg[i]:>10.4f} {a_ref:>10.4f} {a_err:>10.5f}")

    print(f"\nMax voltage magnitude error: {max_v_err:.5f}%")
    return max_v_err


if __name__ == "__main__":
    validate()