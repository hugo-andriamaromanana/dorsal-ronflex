"""Definition of Signal and Spike calc"""

from dataclasses import dataclass
from typing import List

from dorsal_ronflex.spikes.create_spikes import create_spikes
from dorsal_ronflex.spikes.spike import Spikes


@dataclass(frozen = True)
class Signal:
    """Abstract Base Class for vague definitions of signals"""
    spike_tolerence: float
    amps: List[float]
    times: List[float]

    @property
    def spikes(self) -> Spikes:
        """Creating spike object from signals"""
        return create_spikes(self,self.spike_tolerence)
