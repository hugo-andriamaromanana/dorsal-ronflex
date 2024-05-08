"""Handling a complete sweep"""

from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple

from numpy import abs, array, trapz
from pandas import DataFrame

from dorsal_ronflex.signals.signal import Signal
from dorsal_ronflex.signals.spike import Spike, Spikes


def _get_index_of_time(time: float, times: List[float]) -> int:
    """Gets the index of the time."""
    closest_time = _match_time_to_signals(times, time)
    for index, signal_time in enumerate(times):
        if signal_time == closest_time:
            return index
    raise ValueError("Time not found in signals.")


def calc_area_under_curve(sweep: "Sweep", start_time: float, end_time: float) -> float:
    """Calculates the area under the curve."""
    start_index = _get_index_of_time(start_time, sweep.abs_signals.times)
    stop_index = _get_index_of_time(end_time, sweep.abs_signals.times)
    y = sweep.abs_signals.amps[start_index:stop_index]
    x = sweep.abs_signals.times[start_index:stop_index]
    area = trapz(y, x)
    return float(area)


def _find_earliest_spike(all_spikes: List[Spike]) -> Spike:
    """Given a list of spikes, returns the spike with the lowest time"""
    min = all_spikes[0]
    for spike in all_spikes:
        if spike.time < min.time:
            min = spike
    return min


def _find_latest_spike(all_spikes: List[Spike]) -> Spike:
    """Given a list of spikes, returns the spike with the highest time"""
    max = all_spikes[0]
    for spike in all_spikes:
        if spike.time > max.time:
            max = spike
    return max


def _match_time_to_signals(times: List[float], guess: float) -> float:
    """Finds the closest time to the given guess."""
    nd_times = array(times)
    closest_index = abs(nd_times - guess).argmin()
    closest_time = times[int(closest_index)]
    return closest_time


def _find_bounding_spikes(spikes_res: List[Spike]) -> Tuple[Spike, Spike]:
    """Returns the first and last spike in the event"""
    return _find_earliest_spike(spikes_res), _find_latest_spike(spikes_res)


def infer_event_bondaries(sweep: "Sweep") -> Tuple[float, float]:
    """Applies ms delay to exterme spikes, and fits them on the curve"""
    first_spike, last_spike = _find_bounding_spikes(sweep.abs_spikes.res)
    decremented_time = first_spike.time - sweep.ms_delay
    incremented_time = last_spike.time + sweep.ms_delay
    start, end = _match_time_to_signals(
        sweep.abs_signals.times, decremented_time
    ), _match_time_to_signals(sweep.abs_signals.times, incremented_time)
    return start, end


@dataclass
class Sweep:
    """Everything we need from a Sweep"""

    id: int
    raw_signals: Signal
    abs_signals: Signal
    control_area_increment: int
    ms_delay: int

    @cached_property
    def stim(self) -> Spike:
        """Point of stimulation"""
        return self.raw_signals.spikes.stim

    @cached_property
    def raw_spikes(self) -> Spikes:
        """Contains spikes in raw signal"""
        return self.raw_signals.spikes

    @cached_property
    def abs_spikes(self) -> Spikes:
        """Contains spikes in abs signal"""
        return self.abs_signals.spikes

    @cached_property
    def event_bondaries(self) -> Tuple[float, float]:
        """Start time and end time of the event"""
        return infer_event_bondaries(self)

    @cached_property
    def event_duration(self) -> float:
        """Duration of the event"""
        start, end = self.event_bondaries
        return end - start

    @cached_property
    def area(self) -> float:
        """Area under the 2 points of event_bondaries"""
        start, end = self.event_bondaries
        return calc_area_under_curve(self, start, end)

    @cached_property
    def control_area(self) -> float:
        """Calculates areas on set variables"""
        start, end = (
            self.event_bondaries[0],
            self.event_bondaries[0] + self.control_area_increment,
        )
        return calc_area_under_curve(self, start, end)

    def to_df(self) -> DataFrame:
        """Returns a DataFrame representation of the sweep."""
        data = {
            "Sweep ID": [self.id],
            "Stim": [self.stim],
            "Start Time": [self.event_bondaries[0]],
            "End Time": [self.event_bondaries[1]],
            "Event Duration": [self.event_duration],
            "Area": [self.area],
            "Control Area": [self.control_area],
            "Ms Delay": [self.ms_delay],
            "Control Area Increment": [self.control_area_increment],
        }
        return DataFrame(data)

    def to_txt(self) -> str:
        """Returns a string representation of the sweep."""
        raw_spikes = "".join([str(spike) + "\n" for spike in self.raw_spikes.res])
        abs_spikes = "".join([str(spike) + "\n" for spike in self.abs_spikes.res])
        return f"""
----------------------------------------
Sweep ID: {self.id}
Stim: {self.stim}
Raw Tolerence: {self.raw_signals.spike_tolerence}
Abs Tolerance: {self.abs_signals.spike_tolerence}
Start Time: {self.event_bondaries[0]}
End Time: {self.event_bondaries[1]}
Event Duration: {self.event_duration}
Area: {self.area}
Control Area: {self.control_area}
Ms Delay: {self.ms_delay}
Control Area Increment: {self.control_area_increment}

Raw Spikes:
{raw_spikes}
Abs Spikes:
{abs_spikes}
"""
