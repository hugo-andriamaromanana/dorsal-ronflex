"""Analysis module."""

from pathlib import Path
from sys import exit

from loguru import logger
from tqdm import tqdm

from dorsal_ronflex.analyse.simplified_abf import AbfStudy


def is_directory(path: str) -> bool:
    """Check if the path is a directory."""
    return Path(path).is_dir()


def is_file(path: str) -> bool:
    """Check if the path is a file."""
    return Path(path).is_file()


def analyse_and_save_study(
    study_path: str | Path, output: Path, config_path: str | Path
) -> None:
    """Analyse and save the study."""
    try:
        study = AbfStudy(study_path, config_path)
        study.save(output)
    except Exception as e:
        logger.critical(f"Error analysing {study_path}: {e}")
        exit(0)


def analyse_and_save(path: str, output: Path, config: str | Path) -> None:
    """Makes the distinction between a file and a directory.
    If it is a file, analyse and save the study.
    """
    if is_file(path):
        analyse_and_save_study(path, output, config)
    elif is_directory(path):
        for file in tqdm(Path(path).rglob("*.abf")):
            analyse_and_save_study(file, output, config)
    else:
        logger.critical(f"Path {path} is not a file nor directory.")
