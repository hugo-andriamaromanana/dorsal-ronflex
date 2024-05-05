"""Base classes for all events, peaks, sweeps, and procedures."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List
from numpy import float64, floating
from numpy.typing import NDArray


@dataclass
class Signals:
    """Base class for all signals.
    time: NDArray[float]
    amps: NDArray[float]
    """

    times: List[float] = field(default_factory=list)
    amps: List[float] = field(default_factory=list)

@dataclass(frozen=True)
class Spike:
    """Base class for all peaks.
    amp: float
    time: int
    """

    amp: float
    time: float


@dataclass
class Event:
    """Base class for all events.
    stim_time: int (ms)
    start_time: int (ms)
    end_time: int (ms)
    raw_peaks: List[Peak]
    rect_peaks: List[Peak]
    rect_area: float
    """

    stim_time: int
    start_time: int
    end_time: int
    raw_peaks: List[Spike]
    rect_peaks: List[Spike]
    rect_area: float


@dataclass
class Sweep:
    """Base class for all sweeps.
    sweep_number: int
    channel: int
    events: List[Event]
    """

    sweep_number: int
    channel: int
    events: List[Event]


@dataclass
class Procedure:
    """Base class for all procedures.
    name: str
    date: datetime
    """

    name: str
    date: datetime
    sweeps: List[Sweep]
