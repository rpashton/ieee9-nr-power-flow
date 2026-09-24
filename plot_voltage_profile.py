"""
Voltage Profile Plot
Bar chart of bus voltage magnitudes, for visual validation that every
bus sits within the normal operating range (0.95 - 1.05 pu, typical
utility practice).
"""

import matplotlib.pyplot as plt
from newton_raphson import solve_power_flow
from ieee9_data import N_BUS


def plot_voltage_profile():
    result = solve_power_flow(verbose=False)
    V = result["V"]

    buses = list(range(1, N_BUS + 1))

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(buses, V, color="steelblue", edgecolor="black")

    ax.axhline(1.05, color="red", linestyle="--", linewidth=1, label="Upper limit (1.05 pu)")
    ax.axhline(0.95, color="red", linestyle="--", linewidth=1, label="Lower limit (0.95 pu)")

    ax.set_xlabel("Bus Number")
    ax.set_ylabel("Voltage Magnitude (pu)")
    ax.set_title("IEEE 9-Bus System: Voltage Profile")
    ax.set_xticks(buses)
    ax.set_ylim(0.9, 1.1)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("voltage_profile.png", dpi=150)
    print("Saved voltage_profile.png")
    plt.show()


if __name__ == "__main__":
    plot_voltage_profile()