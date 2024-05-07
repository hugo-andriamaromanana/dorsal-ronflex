"""Handling a complete sweep"""

from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from dorsal_ronflex.signals.signal import Signal
from dorsal_ronflex.spikes.spike import Spike, Spikes
from dorsal_ronflex.sweep.area import calc_intergral_on_time
from dorsal_ronflex.sweep.event_bondaries import infer_event_bondaries


@dataclass
class Sweep:
    """Everything we need from a Sweep"""

    id: int
    raw_signals: Signal
    abs_signals: Signal
    curve_check: int
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
    def area(self) -> float:
        """Area under the 2 points of event_bondaries"""
        return calc_intergral_on_time(self)

    @cached_property
    def control_area(self) -> float:
        """Calculates areas on set variables"""
        return 0.1
