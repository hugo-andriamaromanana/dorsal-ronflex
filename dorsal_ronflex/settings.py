"""Settings for the program."""

import json
from pathlib import Path
from typing import TypedDict

SEGMENT_START_STR = "segment_start"
SEGMENT_END_STR = "segment_end"
DEFAULT_CURVE_CHECK_STR = "default_curve_check"
DEFAULT_MS_DELAY_STR = "default_ms_delay"
DEFAULT_TOLERANCE_STR = "default_tolerance"
DEFAULT_ABS_TOLERANCE_STR = "default_abs_tolerance"
DEFAULT_CHANNEL_STR = "default_channel"


class Config(TypedDict):
    """Config for the program."""

    segment_start: int
    segment_end: int
    default_curve_check: int
    default_ms_delay: int
    default_tolerance: float
    default_abs_tolerance: float
    default_channel: int


_DEFAULT_CONFIG: Config = {
    SEGMENT_START_STR: 5568,
    SEGMENT_END_STR: 5668,
    DEFAULT_CURVE_CHECK_STR: 90,
    DEFAULT_MS_DELAY_STR: 5,
    DEFAULT_TOLERANCE_STR: 0.1,
    DEFAULT_ABS_TOLERANCE_STR: 0.15,
    DEFAULT_CHANNEL_STR: 1,
}


class ConfigLoader:
    """Singleton class for loading the config file."""

    _instance = None

    def __new__(cls):
        """Singleton instance."""
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.config = _DEFAULT_CONFIG
        return cls._instance

    def init(self, filepath: str | Path | None) -> None:
        """Initializes the config file."""
        if filepath is None:
            self.config = _DEFAULT_CONFIG
            return None
        filepath = str(filepath)
        with open(filepath) as file:
            self.config = json.load(file)

    def get(self) -> Config:
        """Returns the config."""
        return self.config


_CONFIG_LOADER = ConfigLoader()
_CONFIG_LOADER.init(None)

CONFIG: Config = _CONFIG_LOADER.get()
