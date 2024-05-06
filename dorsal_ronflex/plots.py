"""Module for plotting the signals and spikes."""

from typing import List

import matplotlib.pyplot as plt

from dorsal_ronflex.event import Signals, Spike


def init_plot(signals: Signals) -> None:
    """Initializes the plot."""
    plt.plot(signals.times, signals.amps, lw=2, alpha=0.7, color="b")
    plt.xlabel("Time (ms)")
    plt.ylabel("Amps IN 2 (V)")
    plt.title("Shade a Specific Epoch")


def plot_at_spiker(signals: Signals, spikes: List[Spike]) -> None:
    """Plots the signals at the spikes."""
    init_plot(signals)
    for spike in spikes:
        plt.plot(spike.time, spike.amp, "ro")
    plt.show()
