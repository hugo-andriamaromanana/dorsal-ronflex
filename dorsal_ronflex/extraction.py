"""Extracts the signals from the ABF file."""

from pathlib import Path
from typing import Any, List, Tuple

from icecream import ic
from numpy import floating
from numpy.typing import NDArray
from pyabf import ABF

from dorsal_ronflex.event import Signals, Spike

_MIN_MS_RANGE = 5568
_MAX_MS_RANGE = 5668


def _load_abf_file(file_path: str | Path) -> ABF:
    """Loads the ABF file."""
    return ABF(file_path)


def _to_abs(raw_signals: Signals) -> Signals:
    """Converts the sweepY values from volts to absolute values."""
    new_amps = [abs(amp) for amp in raw_signals.amps]
    return Signals(times=raw_signals.times, amps=new_amps)


def _create_src_signals(
    times: NDArray[floating[Any]], amps: NDArray[floating[Any]]
) -> Signals:
    """Extracts the time and amplitudes from the ABF file.
    Only takes time in between pre determined segment
    """
    new_times = []
    new_amps = []
    for key, value in zip(times, amps):
        time = key * 1000
        if _MIN_MS_RANGE < time < _MAX_MS_RANGE:
            new_times.append(key * 1000)
            new_amps.append(float(value))
    return Signals(new_times, new_amps)


def _create_abs_signals(raw_signals: Signals) -> Signals:
    """Creates the absolute signals."""
    return _to_abs(raw_signals)


def create_signals(abf: ABF) -> Tuple[Signals, Signals]:
    """Creates the raw and absolute signals."""
    source = _create_src_signals(abf.sweepX, abf.sweepY)
    abs_signals = _create_abs_signals(source)
    return source, abs_signals


def _find_spike_successions(signals: Signals, tolerence: float) -> List[List[Spike]]:
    """Finds the spike successions."""
    spikes = []
    ic(len(signals.amps))
    successive_spikes = []
    chain_is_open = False
    for time, amp in zip(signals.times, signals.amps):
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


def find_spikes(signals: Signals, tolerence: float) -> List[Spike]:
    """Finds the spikes."""
    spikes = []
    spike_successions = _find_spike_successions(signals, tolerence)
    for spike_succession in spike_successions:
        largest_spike = max(spike_succession, key=lambda x: x.amp)
        spikes.append(largest_spike)
    return spikes


def find_initial_stim(spikes: List[Spike]) -> Spike:
    """Finds the initial stimulation time."""
    return min(spikes, key=lambda x: x.amp)


# def determine_event_boundaries(raw_signals: Signals) -> Tuple[int, int]:
#     """Determines the start and stop time of the event."""
#     stim = find_initial_stim(raw_signals)
#     return stop_time, start_time

# def extract_procedure():
#     abf = ABF("data/24415011.abf")
#     raw_signals = create_raw_signals(abf)
#     abs_signals = create_abs_signals(abf)
#     stop_time, start_time = determine_event_boundaries(raw_signals)
