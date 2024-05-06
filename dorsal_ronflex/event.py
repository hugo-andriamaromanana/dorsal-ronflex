"""Base classes for all events, peaks, sweeps, and procedures."""

from dataclasses import dataclass, field
from datetime import datetime
from os import mkdir
from os.path import join
from pathlib import Path
from typing import Dict, List

import pandas as pd


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

    sweep_id: int
    stim_time: float
    start_time: float
    end_time: float
    raw_peaks: List[Spike]
    rect_peaks: List[Spike]
    rect_area: float
    control_rect_area: float

    def to_csv(self, output_path: str | Path) -> None:
        """Writes data to CSV files."""
        # Write resume data to CSV
        resume_data = pd.DataFrame(
            {
                "stim_time": [self.stim_time],
                "start_time": [self.start_time],
                "end_time": [self.end_time],
                "rect_area": [self.rect_area],
                "control_rect_area": [self.control_rect_area],
            }
        )
        mkdir(join(output_path, str(self.sweep_id)))
        new_path = join(output_path, str(self.sweep_id))
        resume_data.to_csv(join(new_path, "resume.csv"), index=False)

        # Write raw peaks to JSON
        raw_peaks_data = pd.DataFrame(self.raw_peaks_as_dict, index=[0])
        raw_peaks_data.to_json(
            join(new_path, "raw_peaks.json"), orient="records", indent=4
        )

        # Write rect peaks to JSON
        rect_peaks_data = pd.DataFrame(self.rect_spikes_as_dict, index=[0])
        rect_peaks_data.to_json(
            join(new_path, "rect_peaks.json"), orient="records", indent=4
        )

    @property
    def raw_peaks_as_dict(self) -> Dict[float, float]:
        """Returns a dictionary of spikes."""
        return {spike.time: spike.amp for spike in self.raw_peaks}

    @property
    def rect_spikes_as_dict(self) -> Dict[float, float]:
        """Returns a dictionary of spikes."""
        return {spike.time: spike.amp for spike in self.rect_peaks}


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
