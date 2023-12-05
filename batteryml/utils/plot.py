import random
import numpy as np
import matplotlib.pyplot as plt

from itertools import cycle as cycle_iterator


def plot_multiple_y_axis(*y_data, fig=None, ax=None, x=None, curve_names=None, colors=None):
    """
    Plots multiple curves each with its own y-axis.

    :param y_data: A list of y-axis data arrays, one for each curve.
    :param x: Optional common x-axis data for all curves. If None, use np.arange(len(curve)).
    :param curve_names: Optional list of names for the curves.
    :param colors: Optional list of colors for each curve.
    """

    if x is None:
        x = np.arange(len(y_data[0]))

    if curve_names is None:
        curve_names = [f"Curve {i+1}" for i in range(len(y_data))]

    if colors is None:
        color_cycle = cycle_iterator(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        colors = [next(color_cycle) for _ in range(len(y_data))]

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    axes = [ax]

    for i, y in enumerate(y_data):
        if i != 0:
            # Create a new y-axis
            axes.append(ax.twinx())
            # Position the y-axis
            axes[-1].spines['right'].set_position(('outward', 60 * (i - 1)))

        # Plotting the curve
        axes[i].plot(x, y, color=colors[i])
        axes[i].set_ylabel(curve_names[i], color=colors[i])
        axes[i].tick_params(axis='y', labelcolor=colors[i])

        # Random adjust ylim
        ymin, ymax = axes[i].get_ylim()
        shift = (ymax - ymin) / 25 * random.random()
        axes[i].set_ylim(ymin + shift, ymax + shift)
        

    axes[0].grid()
    plt.tight_layout()

    return fig, axes