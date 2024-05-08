"""File Handling sweep creation"""

from typing import Any

from numpy import floating
from numpy.typing import NDArray

from dorsal_ronflex.settings import (
    CONFIG,
    DEFAULT_ABS_TOLERANCE_STR,
    DEFAULT_CURVE_CHECK_STR,
    DEFAULT_MS_DELAY_STR,
    DEFAULT_TOLERANCE_STR,
    SEGMENT_END_STR,
    SEGMENT_START_STR,
)
from dorsal_ronflex.signals.create_signals import create_abs_signal, create_signal
from dorsal_ronflex.sweep.sweep import Sweep

_INTERVAL = CONFIG[SEGMENT_START_STR], CONFIG[SEGMENT_END_STR]
_DEFAULT_TOLERANCE = CONFIG[DEFAULT_TOLERANCE_STR]
_DEFAULT_ABS_TOLERANCE = CONFIG[DEFAULT_ABS_TOLERANCE_STR]
_DEFAULT_CURVE_CHECK = CONFIG[DEFAULT_CURVE_CHECK_STR]
_DEFAULT_MS_DELAY = CONFIG[DEFAULT_MS_DELAY_STR]


def create_sweep(
    id: int, times: NDArray[floating[Any]], amps: NDArray[floating[Any]]
) -> Sweep:
    """Creates different signals and starts the sweep"""
    raw_signals = create_signal(times, amps, _INTERVAL, _DEFAULT_TOLERANCE)
    abs_signals = create_abs_signal(
        times,
        amps,
        _INTERVAL,
        _DEFAULT_ABS_TOLERANCE,
    )
    return Sweep(
        id,
        raw_signals,
        abs_signals,
        _DEFAULT_CURVE_CHECK,
        _DEFAULT_MS_DELAY,
    )
