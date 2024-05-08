"""Definition of Spike and associated methods"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Spike:
    """Definition of a spike"""

    amp: float
    time: float

@dataclass(frozen=True)
class Spikes:
    """Contains the stimulation spike
    and the rest of the spikes
    """

    stim: Spike
    res: List[Spike]
