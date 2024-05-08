"""Argument parsing and main function for the dorsal_ronflex package."""

from argparse import ArgumentParser
from pathlib import Path

from dorsal_ronflex.analyse.analysis import analyse_and_save


def main() -> None:
    """Main function for the dorsal_ronflex package."""
    parser = ArgumentParser(description="Dorsal Ronflex")

    parser.add_argument(
        "path",
        type=Path,
        help="Path to the ABF file or directory containing ABF files.",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output",
        default=".",
        type=Path,
        help="Path to the output directory.",
    )

    parser.add_argument(
        "-c",
        "--config",
        default=None,
        type=Path,
        help="Path to the config file.",
    )

    args = parser.parse_args()
    path = args.path
    output = args.output
    config = args.config

    analyse_and_save(path, output, config)


if __name__ == "__main__":
    main()
