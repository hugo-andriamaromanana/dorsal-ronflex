"""Cli for ABF Parser"""

from argparse import ArgumentParser
from pathlib import Path

from loguru import logger

from dorsal_ronflex.extraction import (
    extract_all_sweeps_from_config,
    extract_all_sweeps_from_file,
)


def main():
    """Main function for the cli."""
    parser = ArgumentParser(
        prog="ABF Parser",
        description="Takes a config path as in an input and"
        + "an output path as an output and parses the ABF file.",
        epilog="Made with love <3",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_path",
        required=False,
        type=Path,
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        required=False,
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        type=Path,
    )

    args = parser.parse_args()

    config_path = args.config_path
    output_path = args.output_path
    input_path = args.input_path

    if config_path:
        extract_all_sweeps_from_config(config_path, output_path)
    elif input_path:
        extract_all_sweeps_from_file(input_path, output_path)

    else:
        logger.error("Please provide a config or an input path.")


if __name__ == "__main__":
    main()
