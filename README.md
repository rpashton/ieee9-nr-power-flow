# Newton-Raphson Power Flow Solver

A Newton-Raphson load flow solver built from scratch in Python for the
IEEE 9-bus standard test system where it computes bus voltages, angles,
line flows, and system losses without relying on other power systems
toolboxes.

## Results

- Converges in **4 iterations** from a flat start (1.0 pu, 0°)
- Validated against an independent reference solution (MATPOWER case9,
  solved via pandapower): **maximum voltage magnitude error of 0.00004%**
- Total system real power losses: **4.95 MW**, verified via energy
  balance (generation = load + losses, matching to 4 decimal places)
- All of the 9 bus voltages fall within the ANSI C84.1 ±5% operating band

![Voltage Profile] (voltage_profile.png)

## What it does

1. **Builds the bus admittance matrix (Ybus)** from line and transformer
   impedance data, using the standard branch-stamping procedure
2. **Solves the nonlinear power flow equations** iteratively using
   Newton-Raphson, with an analytically-derived Jacobian (not numerical
   differentiation)
3. **Computes line power flows and losses** on every branch
4. **Validates** the converged solution against a known-correct reference
5. **Visualizes** the voltage profile against standard utility operating limits

## Tech stack

Python, NumPy (matrix operations, linear system solving), Matplotlib
(visualization)

## File structure

| File | Purpose |
| `ieee9_data.py` | IEEE 9-bus system data (buses, lines, transformers) |
| `ybus.py` | Bus admittance matrix builder |
| `power_equations.py` | Power injection equations (P, Q from V, θ) |
| `jacobian.py` | Newton-Raphson Jacobian matrix builder |
| `newton_raphson.py` | Main iterative solver |
| `validate.py` | Validation against reference solution |
| `line_flows.py` | Line power flow and loss calculations |
| `plot_voltage_profile.py` | Voltage profile visualization |

## How to run

```bash
pip install numpy matplotlib
python newton_raphson.py       # run the solver
python validate.py             # check accuracy against reference
python line_flows.py           # compute line flows and losses
python plot_voltage_profile.py # generate voltage profile plot
```

## Method

The solver implements the standard Newton-Raphson power flow algorithm:
given specified power injections at every bus, it iteratively solves
for the unknown voltage magnitudes (at PQ buses) and angles (at PQ buses) and angles (at all
non-slack buses) by linearizing the nonlinear power balance equations
at each step using the Jacobian, then solving the resulting linear
system for a correction to the current guess. The process repeats
until the mismatch between specified and calculated power falls below
1e-6 pu.

## Author

Rahman Pashton
