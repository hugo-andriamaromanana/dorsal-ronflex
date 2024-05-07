"""Spikes Creation"""

from typing import List

from dorsal_ronflex.signals.signal import Signal
from dorsal_ronflex.spikes.spike import Spike, Spikes


def _find_highest_spike_stim_index(spikes: List[Spike]) -> int:
    """Finds the largest stimulation time."""
    max = 0
    for index, spike in enumerate(spikes):
        if spike.time > spikes[max].time:
            max = index
    return max


def _create_spike_successions(signal: Signal, tolerence: float) -> List[List[Spike]]:
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


def _create_all_spikes(signals: Signal, tolerence: float) -> List[Spike]:
    """Finds the spikes from the successions by taking the highest spikes
    in all the sucessions
    """
    spikes = []
    spike_successions = _create_spike_successions(signals, tolerence)
    for spike_succession in spike_successions:
        largest_spike = max(spike_succession, key=lambda x: x.amp)
        spikes.append(largest_spike)
    return spikes


def create_spikes(signals: Signal, tolerence: float) -> Spikes:
    """Spikes creation, gets all the spikes then splits the stimulation"""
    all_spikes = _create_all_spikes(signals, tolerence)
    stim_index = _find_highest_spike_stim_index(all_spikes)
    stim = all_spikes.pop(stim_index)
    return Spikes(stim, all_spikes)
