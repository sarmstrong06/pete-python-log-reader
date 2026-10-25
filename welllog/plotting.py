"""Plotting helpers for well log data."""

import matplotlib.pyplot as plt


def plot_logs(data, curves, units=None, depth=None, title=None):
    """Plot log curves side by side against depth.

    data   : DataFrame with one column per curve, including depth
    curves : list of column names to plot, one track each
    units  : optional dict of {column name: unit}; resistivity (ohm) tracks
             are drawn on a log scale
    depth  : name of the depth column (defaults to the first column)
    title  : optional figure title, e.g. the well name
    """
    units = units or {}
    depth = depth or data.columns[0]

    fig, axes = plt.subplots(1, len(curves), sharey=True,
                             figsize=(2.5 * len(curves), 7), squeeze=False)
    axes = axes[0]

    for ax, name in zip(axes, curves):
        if name not in data.columns:
            raise KeyError(f'Curve "{name}" is not in the data.')
        unit = units.get(name, "")
        ax.plot(data[name], data[depth], linewidth=1)
        ax.set_xlabel(f"{name} ({unit})" if unit else name)
        ax.xaxis.set_label_position("top")
        ax.xaxis.tick_top()
        ax.grid(True, which="both", alpha=0.3)
        if "OHM" in unit.upper():
            ax.set_xscale("log")

    axes[0].set_ylabel(f"Depth ({units.get(depth, '')})" if units.get(depth) else "Depth")
    axes[0].set_ylim(data[depth].max(), data[depth].min())  # depth increases downward
    if title:
        fig.suptitle(title)
    fig.tight_layout()
    return fig
