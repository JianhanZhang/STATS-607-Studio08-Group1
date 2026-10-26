"""Studio 08: Three-panel plot for ridgeless-regression risk.

Full assignment:
    python analyze_results.py

Small demonstration:
    python analyze_results.py --input demo_results.pkl --output demo_figure.pdf
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

R2 = 5.0


def add_theory(ax) -> None:
    left = np.geomspace(0.1, 0.99, 400)
    right = np.geomspace(1.01, 10.0, 400)
    ax.plot(left, left / (1.0 - left), color="black", lw=1.6, label="Theory")
    ax.plot(right, R2 * (1.0 - 1.0 / right) + 1.0 / (right - 1.0),
            color="black", lw=1.6)
    ax.axvline(1.0, color="black", linestyle="--", lw=1, alpha=0.7)
    ax.set_xscale("log")  # [0.1,1] and [1,10] occupy equal widths.
    ax.set_xlim(0.1, 10.0)
    ax.set_xticks([0.1, 1.0, 10.0], labels=["0.1", "1", "10"])
    ax.set_ylim(0, 30)  # Clip very large errors near interpolation threshold.
    ax.set_xlabel(r"$\gamma=p/n$")
    ax.grid(alpha=0.15)


def plot_data(ax, frame: pd.DataFrame, n_sim: int) -> None:
    if n_sim == 1:
        ax.scatter(frame["gamma"], frame["MSE"], s=5, alpha=0.12,
                   label="Single trial")
        # Smooth each side separately to avoid smoothing across the asymptote.
        for lower, upper in ((0.1, 1.0), (1.0, 10.0)):
            side = frame[(frame["gamma"] >= lower) & (frame["gamma"] <= upper)]
            if len(side) >= 5:
                curve = lowess(side["MSE"], side["gamma"],
                               frac=0.1, it=0, return_sorted=True)
                ax.plot(curve[:, 0], curve[:, 1], color="tab:orange", lw=2,
                        label="LOWESS" if lower == 0.1 else None)
    else:
        ax.errorbar(frame["gamma"], frame["MSE"], yerr=2.0 * frame["se"],
                    fmt="o", markersize=3, capsize=2, elinewidth=0.8,
                    alpha=0.8, label=r"Monte Carlo $\pm 2$ SE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("results/raw/simulation_results.pkl"))
    parser.add_argument("--output", type=Path, default=Path("results/figures/figure.pdf"))
    args = parser.parse_args()

    df = pd.read_pickle(args.input)
    required = {"n_sim", "gamma", "MSE", "se"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing DataFrame columns: {required - set(df.columns)}")
    regimes = sorted(df["n_sim"].unique())
    if len(regimes) != 3:
        raise ValueError("Expected exactly three n_sim regimes")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True, layout="constrained")
    for ax, n_sim in zip(axes, regimes):
        subset = df.loc[df["n_sim"] == n_sim].sort_values("gamma")
        plot_data(ax, subset, int(n_sim))
        add_theory(ax)
        ax.set_title(rf"$n_{{\mathrm{{sim}}}}={int(n_sim)}$")
        ax.legend(loc="upper right", frameon=False, fontsize=8)
    axes[0].set_ylabel(r"Risk $\|\hat\beta-\beta\|^2$")
    fig.savefig(args.output, bbox_inches="tight")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
