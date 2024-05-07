"""File handling all area calculations"""

from typing import List

from numpy import trapz

from dorsal_ronflex.sweep.sweep import Sweep


def _get_index_of_time(time: float, times: List[float]) -> int:
    """Gets the index of the time."""
    for index, signal_time in enumerate(times):
        if signal_time == time:
            return index
    raise ValueError("Time not found in signals.")

def calc_intergral_on_time(sweep: Sweep) -> float:
    """Finds the area under the curve."""
    start_time,end_time = sweep.event_bondaries
    start_index = _get_index_of_time(start_time, sweep.abs_signals.times)
    stop_index = _get_index_of_time(end_time, sweep.abs_signals.times)
    y = sweep.abs_signals.amps[start_index:stop_index]
    x = sweep.abs_signals.times[start_index:stop_index]
    area = trapz(y, x)
    return float(area)
