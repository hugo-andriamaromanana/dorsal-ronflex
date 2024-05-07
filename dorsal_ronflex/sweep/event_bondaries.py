"""File handling events bounds"""

from typing import List, Tuple

from numpy import abs, array

from dorsal_ronflex.spikes.spike import Spike
from dorsal_ronflex.sweep.sweep import Sweep


def _find_earliest_spike(all_spikes: List[Spike]) -> Spike:
    """Given a list of spikes, returns the spike with the lowest time"""
    min = all_spikes[0]
    for spike in all_spikes:
        if spike.time < min.time:
            min = spike
    return min


def _find_latest_spike(all_spikes: List[Spike]) -> Spike:
    """Given a list of spikes, returns the spike with the highest time"""
    min = all_spikes[0]
    for spike in all_spikes:
        if spike.time > min.time:
            min = spike
    return min


def _match_time_to_signals(times: List[float], guess: float) -> float:
    """Finds the closest time to the given guess."""
    nd_times = array(times)
    closest_index = abs(nd_times - guess).argmin()
    closest_time = times[int(closest_index)]
    return closest_time


def _find_bounding_spikes(spikes_res: List[Spike]) -> Tuple[Spike, Spike]:
    """Returns the first and last spike in the event"""
    return _find_earliest_spike(spikes_res), _find_latest_spike(spikes_res)


def infer_event_bondaries(sweep: Sweep) -> Tuple[float, float]:
    """Applies ms delay to exterme spikes, and fits them on the curve"""
    first_spike, last_spike = _find_bounding_spikes(sweep.abs_spikes.res)
    decremented_time = first_spike.time - sweep.ms_delay
    incremented_time = last_spike.time + sweep.ms_delay
    return _match_time_to_signals(
        sweep.abs_signals.times, decremented_time
    ), _match_time_to_signals(sweep.abs_signals.times, incremented_time)

