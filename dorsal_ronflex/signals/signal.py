"""Definition of Signal and Spike calc"""

from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt

from dorsal_ronflex.signals.spike import Spike, Spikes


def _find_max_amp_index(spikes: list[Spike]) -> int:
    """Finds the index of the spike with the highest amplitude."""
    max_amp = 0
    max_index = 0
    for index, spike in enumerate(spikes):
        if spike.amp > max_amp:
            max_amp = spike.amp
            max_index = index
    return max_index


def _create_spike_successions(signal: "Signal", tolerence: float) -> List[List[Spike]]:
    """Finds the spike successions, which is a 2D array containing all spikes found"""
    spikes = []
    successive_spikes = []
    chain_is_open = False
    for time, amp in zip(signal.times, signal.amps):
        is_spike = amp > tolerence
        if is_spike:
            if not chain_is_open:
                chain_is_open = True
            successive_spikes.append(Spike(amp=amp, time=time))
        elif chain_is_open:
            spikes.append(successive_spikes)
            successive_spikes = []
            chain_is_open = False
    return spikes


def _create_all_spikes(signals: "Signal", tolerence: float) -> List[Spike]:
    """Finds the spikes from the successions by taking the highest spikes
    in all the sucessions
    """
    spikes = []
    spike_successions = _create_spike_successions(signals, tolerence)
    for spike_succession in spike_successions:
        largest_spike = max(spike_succession, key=lambda x: x.amp)
        spikes.append(largest_spike)
    return spikes


def _create_spikes(signals: "Signal", tolerence: float) -> Spikes:
    """Spikes creation, gets all the spikes then splits the stimulation"""
    all_spikes = _create_all_spikes(signals, tolerence)
    stim_index = _find_max_amp_index(all_spikes)
    stim = all_spikes.pop(stim_index)
    return Spikes(stim, all_spikes)


@dataclass(frozen=True)
class Signal:
    """Abstract Base Class for vague definitions of signals"""

    spike_tolerence: float
    amps: List[float]
    times: List[float]

    @property
    def spikes(self) -> Spikes:
        """Creating spike object from signals"""
        return _create_spikes(self, self.spike_tolerence)

    def plot(self, spikes: List[Spike]) -> None:
        """Initializes the plot with the signal and spikes"""
        plt.plot(self.times, self.amps, lw=2, alpha=0.7, color="b")
        plt.xlabel("Time (ms)")
        plt.ylabel("Amps IN 2 (V)")
        plt.title("Shade a Specific Epoch")
        for spike in spikes:
            plt.plot(spike.time, spike.amp, "ro")
        plt.show()
