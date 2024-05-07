"""Signal treatment and creation"""

from typing import Any, List, Tuple

from numpy import floating
from numpy.typing import NDArray

from dorsal_ronflex.signals.signal import Signal


def _crop_and_format_signal(
    times: NDArray[floating[Any]],
    amps: NDArray[floating[Any]],
    interval: Tuple[int, int],
) -> Tuple[List[float], List[float]]:
    """From raw signals returns the same signals in the designated interval"""
    min_ms_range, max_ms_range = interval
    new_times = []
    new_amps = []
    for key, value in zip(times, amps):
        time = key * 1000
        if min_ms_range < time < max_ms_range:
            new_times.append(key * 1000)
            new_amps.append(float(value))
    return new_times, new_amps


def create_signal(
    times: NDArray[floating[Any]],
    amps: NDArray[floating[Any]],
    interval: Tuple[int, int],
    spike_tolerence: float,
) -> Signal:
    """With the set interval, and spike tolerence creates Signal object"""
    new_times, new_amps = _crop_and_format_signal(times, amps, interval)
    return Signal(spike_tolerence, new_amps, new_times)


def create_abs_signal(
    times: NDArray[floating[Any]],
    amps: NDArray[floating[Any]],
    interval: Tuple[int, int],
    spike_tolerence: float,
) -> Signal:
    """Applies absolute value to all amps"""
    signal = create_signal(times,amps,interval,spike_tolerence)
    new_amps = [abs(amp) for amp in signal.amps]
    return Signal(signal.spike_tolerence, new_amps, signal.times)
