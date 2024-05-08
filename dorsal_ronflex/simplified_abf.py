from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from pathlib import Path
from pyabf import ABF
from typing import List

from loguru import logger

from dorsal_ronflex.sweep.create_sweep import create_sweep
from dorsal_ronflex.sweep.sweep import Sweep

_DEFAULT_CHANNEL = 1

def load_abf(abf_file: str | Path) -> ABF:
    """Load an ABF file and return the ABF object."""
    abf = ABF(abf_file)
    return abf

@dataclass
class AbfStudy:
    """Everything we need from a study."""
    filepath: str | Path

    @cached_property
    def abf(self) -> ABF:
        """Load an ABF file and return the ABF object."""
        return load_abf(self.filepath)

    @cached_property
    def name(self) -> str:
        """Name of the file."""
        return self.abf.abfID

    @cached_property
    def sweep_count(self) -> int:
        """Number of sweeps in the file."""
        if isinstance(count := self.abf.sweepCount, (int, float)) and count > 0:
            return int(count)
        raise ValueError("Sweep count is not a positive integer.")

    @cached_property
    def abd_start_time(self) -> datetime | None:
        """Start time of the file."""
        if isinstance(start_time := self.abf.abfDateTime, datetime):
            return start_time
        logger.warning("Start time is not a datetime | str object.")
        return None

    @cached_property
    def protocol(self) -> str:
        """Protocol of the file."""
        return self.abf.protocol

    @cached_property
    def adc_name(self) -> str:
        """Name of the ADC channel."""
        return self.abf.adcNames[_DEFAULT_CHANNEL]
    
    @cached_property
    def adc_units(self) -> str:
        """"Units of the ADC channel."""
        return self.abf.adcUnits[_DEFAULT_CHANNEL]
    
    @cached_property
    def sweep_data(self) -> List[Sweep]:
        """Data of the sweeps."""
        sweep_data = []
        for sweep_number in range(self.sweep_count):
            self.abf.setSweep(sweep_number, channel = _DEFAULT_CHANNEL)
            sweep = create_sweep(sweep_number, self.abf.sweepX, self.abf.sweepY)
            sweep_data.append(sweep)
        return sweep_data
    