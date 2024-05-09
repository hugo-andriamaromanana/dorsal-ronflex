"""Simplified ABF file handling."""

from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from os import mkdir
from os.path import join
from pathlib import Path
from typing import List

from genericpath import exists
from loguru import logger
from pandas import DataFrame, concat
from pyabf import ABF

from dorsal_ronflex.settings import CONFIG, DEFAULT_CHANNEL_STR, ConfigLoader
from dorsal_ronflex.sweep.create_sweep import create_sweep
from dorsal_ronflex.sweep.sweep import Sweep

_DEFAULT_CHANNEL = CONFIG[DEFAULT_CHANNEL_STR]


def generate_unique_dirname(directory: str, dirname: str) -> str:
    """Generate a unique directory name by appending a number
    if directory already exists.
    """
    counter = 1
    new_dirname = dirname
    while exists(join(directory, new_dirname)):
        new_dirname = f"{dirname}_{counter}"
        counter += 1
    return new_dirname


def load_abf(abf_file: str | Path) -> ABF:
    """Load an ABF file and return the ABF object."""
    abf = ABF(abf_file)
    return abf


@dataclass
class AbfStudy:
    """Everything we need from a study."""

    filepath: str | Path
    config_filepath: str | Path | None = None

    @cached_property
    def abf(self) -> ABF:
        """Load an ABF file and return the ABF object."""
        ConfigLoader().init(self.config_filepath)
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
        """Units of the ADC channel."""
        return str(self.abf.adcUnits[_DEFAULT_CHANNEL])

    @cached_property
    def sweep_data(self) -> List[Sweep]:
        """Data of the sweeps."""
        sweep_data = []
        logger.info(f"Creating sweep data for {self.name}")
        for sweep_number in range(self.sweep_count):
            self.abf.setSweep(sweep_number, channel=_DEFAULT_CHANNEL)
            sweep = create_sweep(sweep_number, self.abf.sweepX, self.abf.sweepY)
            sweep_data.append(sweep)
        logger.info(f"Finished {self.sweep_count} sweeps.")
        return sweep_data

    def sweep_repr(self) -> str:
        """Representation of the sweep data."""
        return "\n".join(sweep.to_txt() for sweep in self.sweep_data)

    def to_txt(self) -> str:
        """Returns a string representation of the study."""
        return f"""
Study: {self.name}
Protocol: {self.protocol}
Start time: {self.abd_start_time}
ADC Name: {self.adc_name}
ADC Units: {self.adc_units}
Sweep Count: {self.sweep_count}
{self.sweep_repr()}
"""

    def to_df(self) -> DataFrame:
        """Returns a DataFrame representation of the study."""
        data = []
        for i, sweep in enumerate(self.sweep_data):
            first_part = DataFrame(
                {
                    "Study": [self.name],
                    "Sweep Number": [sweep.id],
                    "ABD Start Time": [self.abd_start_time],
                    "Protocol": [self.protocol],
                    "ADC Name": [self.adc_name],
                    "ADC Units": [self.adc_units],
                    "Sweep Count": [self.sweep_count],
                    "Sweep ID": [i],
                }
            )
            second_part = sweep.to_df()
            merged_df = concat([first_part, second_part], axis=1)
            data.append(merged_df)
        return concat(data, ignore_index=True)

    def save(self, destination: str | Path) -> None:
        """Save the study to a file."""
        unique_dirname = generate_unique_dirname(str(destination), self.name)
        output_dir = join(destination, unique_dirname)

        txt_name = f"{self.name}.txt"
        csv_name = f"{self.name}.csv"
        txt_destination = join(output_dir, txt_name)
        csv_destination = join(output_dir, csv_name)

        try:
            txt_export = self.to_txt()
            csv_export = self.to_df()
        except Exception as e:
            logger.error(f"Error exporting study {self.name}: {e}")
            raise e

        mkdir(output_dir)
        with open(txt_destination, "w") as file:
            file.write(txt_export)

        with open(csv_destination, "w") as file:
            csv_export.to_csv(file)

        logger.info(f"Study {self.name} saved to {output_dir}")
