"""File Handling sweep creation"""

from typing import Any

from numpy import floating
from numpy.typing import NDArray

from dorsal_ronflex.signals.create_signals import create_abs_signal, create_signal
from dorsal_ronflex.sweep.sweep import Sweep

_MIN_MS_RANGE = 5568
_MAX_MS_RANGE = 5668
_DEFAULT_CURVE_CHECK = 90
_DEFAULT_MS_DELAY = 5
_DEFAULT_TOLERANCE = 0.1
_DEFAULT_ABS_TOLERANCE = 0.15

_INTERVAL = (_MIN_MS_RANGE, _MAX_MS_RANGE)


def create_sweep(
    id: int, times: NDArray[floating[Any]], amps: NDArray[floating[Any]]
) -> Sweep:
    """Creates different signals and starts the sweep"""
    raw_signals = create_signal(times, amps, _INTERVAL, _DEFAULT_TOLERANCE)
    abs_signals = create_abs_signal(times, amps, _INTERVAL, _DEFAULT_ABS_TOLERANCE)
    return Sweep(id, raw_signals, abs_signals, _DEFAULT_CURVE_CHECK, _DEFAULT_MS_DELAY)
