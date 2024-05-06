"""Extracts the signals from the ABF file."""

from os import mkdir
from os.path import join
from pathlib import Path
from typing import Any, List, Tuple

import numpy as np
from loguru import logger
from numpy import floating
from numpy.typing import NDArray
from pyabf import ABF

from dorsal_ronflex.event import Event, Signals, Spike

_MIN_MS_RANGE = 5568
_MAX_MS_RANGE = 5668
_DEFAULT_CURVE_CHECK = 90
_DEFAULT_MS_DELAY = 5
_DEFAULT_TOLERANCE = 0.1
_DEFAULT_ABS_TOLERANCE = 0.15
_CHANNEL = 1


def load_abf_file(file_path: str | Path) -> ABF:
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


def _find_smallest_stim_index(spikes: List[Spike]) -> int:
    """Finds the smallest stimulation time."""
    min = 0
    for index, spike in enumerate(spikes):
        if spike.time < spikes[min].time:
            min = index
    return min


def _find_largest_stim_index(spikes: List[Spike]) -> int:
    """Finds the largest stimulation time."""
    max = 0
    for index, spike in enumerate(spikes):
        if spike.time > spikes[max].time:
            max = index
    return max


def split_stimulus(spikes: List[Spike]) -> Tuple[List[Spike], Spike]:
    """Splits the stimulus."""
    initial = _find_smallest_stim_index(spikes)
    stim = spikes.pop(initial)
    return spikes, stim


def find_closest_spike_time(spikes: List[Spike], guess: float) -> float:
    """Finds the closest spike time to the given guess."""
    times = np.array([spike.time for spike in spikes])
    closest_index = (np.abs(times - guess)).argmin()
    closest_time = times[closest_index]
    return closest_time


def find_closest_time(times: List[float], guess: float) -> float:
    """Finds the closest time to the given guess."""
    nd_times = np.array(times)
    closest_index = (np.abs(nd_times - guess)).argmin()
    closest_time = times[closest_index]
    return closest_time


def get_index_of_time(time: float, signals: Signals) -> int:
    """Gets the index of the time."""
    for index, signal_time in enumerate(signals.times):
        if signal_time == time:
            return index
    raise ValueError("Time not found in signals.")


def calc_intergral_on_time(
    abs_signals: Signals, start_time: float, stop_time: float
) -> float:
    """Finds the area under the curve."""
    start_index = get_index_of_time(start_time, abs_signals)
    stop_index = get_index_of_time(stop_time, abs_signals)
    y = abs_signals.amps[start_index:stop_index]
    x = abs_signals.times[start_index:stop_index]
    area = np.trapz(y, x)
    return area


def determine_event_bondaries(
    abs_signals: Signals, abs_spikes: List[Spike]
) -> Tuple[float, float]:
    """Determines the event bondaries."""
    start_time_guess = (
        abs_spikes[_find_smallest_stim_index(abs_spikes)].time - _DEFAULT_MS_DELAY
    )
    stop_time_guess = (
        abs_spikes[_find_largest_stim_index(abs_spikes)].time + _DEFAULT_MS_DELAY
    )
    stop_time, start_time = find_closest_time(
        abs_signals.times, stop_time_guess
    ), find_closest_time(abs_signals.times, start_time_guess)
    return start_time, stop_time


def find_area_under_curve(
    abs_signals: Signals, event_bondaries: Tuple[float, float]
) -> float:
    """Finds the area under the curve."""
    start_time, stop_time = event_bondaries
    return calc_intergral_on_time(abs_signals, start_time, stop_time)


def validate_fixed_curve(abs_signals: Signals, abs_spikes: List[Spike]) -> float:
    """Validates the fixed curve."""
    start_time_guess = (
        abs_spikes[_find_smallest_stim_index(abs_spikes)].time - _DEFAULT_MS_DELAY
    )
    stop_time_guess = (
        abs_spikes[_find_largest_stim_index(abs_spikes)].time + _DEFAULT_CURVE_CHECK
    )
    stop_time, start_time = find_closest_time(
        abs_signals.times, stop_time_guess
    ), find_closest_time(abs_signals.times, start_time_guess)

    return calc_intergral_on_time(abs_signals, start_time, stop_time)


def create_event(abf: ABF, sweep_nb: int) -> Event:
    """Extracts the procedure."""
    abf.setSweep(sweep_nb, channel=_CHANNEL)
    raw_signals, abs_signals = create_signals(abf)
    raw_spikes = find_spikes(raw_signals, _DEFAULT_TOLERANCE)
    abs_spikes = find_spikes(abs_signals, _DEFAULT_ABS_TOLERANCE)
    abs_spikes, stim = split_stimulus(abs_spikes)
    event_bondaries = determine_event_bondaries(abs_signals, abs_spikes)
    rect_area = find_area_under_curve(abs_signals, event_bondaries)
    control_rect_area = validate_fixed_curve(abs_signals, abs_spikes)
    start_time, stop_time = event_bondaries
    return Event(
        sweep_id=sweep_nb,
        stim_time=stim.time,
        start_time=start_time,
        end_time=stop_time,
        raw_peaks=raw_spikes,
        rect_peaks=abs_spikes,
        rect_area=rect_area,
        control_rect_area=control_rect_area,
    )


def extract_all_sweeps(abf: ABF) -> List[Event]:
    """Extracts all sweeps."""
    events = []
    count = abf.sweepCount
    if isinstance(count, (float, int)):
        for sweep_nb in range(int(count)):
            event = create_event(abf, sweep_nb)
            events.append(event)
    return events


def extract_all_sweeps_from_file(file_path: Any, output_path: Any) -> None:
    """Extracts all sweeps from a file."""
    abf = load_abf_file(file_path)
    events = extract_all_sweeps(abf)
    path = Path(file_path)
    name = path.stem
    mkdir(name)
    new_path = join(output_path, name)
    for event in events:
        event.to_csv(new_path)
    logger.info(f"Data extracted at {output_path}")


def extract_all_sweeps_from_files(file_paths: List[str], output_path: Any) -> None:
    """Extracts all sweeps from a list of files."""
    for file_path in file_paths:
        extract_all_sweeps_from_file(file_path, output_path)


def extract_all_sweeps_from_config(config_path: Any, output_path: Any) -> None:
    """Extracts all sweeps from a config file."""
    with open(config_path) as file:
        file_paths = file.readlines()
    return extract_all_sweeps_from_files(file_paths, output_path)
