hugo-andriamaromanana: @workspace  generate read me, as you can see in the cli we can enter a config file with a path ect... Make it clear and intermediate level

GitHub Copilot: Deciding which workspace information to collect

Collecting workspace information

Filtering to most relevant information

# Dorsal Ronflex

Dorsal Ronflex is a Python package for analyzing ABF files. It provides a set of tools for loading, analyzing, and saving studies from ABF files.

## Installation

To install Dorsal Ronflex, you can use the provided [``install.sh``](install.sh) script:

```sh
./install.sh
```

## Usage

You can use Dorsal Ronflex from the command line using the [`dorsal-ronflex`] command. The command takes a path to an ABF file or a directory containing ABF files as its main argument:

```sh
dorsal-ronflex path/to/your/abf/files
```

### Options

- `-o`, `--output`: Specifies the path to the output directory. By default, the output is saved in the current directory.

```sh
dorsal-ronflex path/to/your/abf/files -o path/to/output/directory
```

- `-c`, `--config`: Specifies the path to a configuration file. The configuration file is a JSON file that can be used to customize various aspects of the analysis. If no configuration file is provided, the program uses default settings.

```sh
dorsal-ronflex path/to/your/abf/files -c path/to/config.json
```

## Configuration

The configuration file is a JSON file that can contain the following keys:

- [`segment_start`]: The start of the segment.
- [`segment_end`]: The end of the segment.
- [`default_curve_check`]: The default curve check value.
- [`default_ms_delay`]: The default millisecond delay.
- [`default_tolerance`]: The default tolerance.
- [`default_abs_tolerance`]: The default absolute tolerance.
- [`default_channel`]: The default channel.

Here is an example of a configuration file:

```json
{
    "segment_start": 5568,
    "segment_end": 5668,
    "default_curve_check": 90,
    "default_ms_delay": 5,
    "default_tolerance": 0.1,
    "default_abs_tolerance": 0.14,
    "default_channel": 1
}
```

You can find an example configuration file in the here: [`docs/example_config.json`](/docs/example_config.json).

## Installation

To install Dorsal Ronflex, you can use the provided `install.sh` script:

```sh
./install.sh
```

## Usage

You can use Dorsal Ronflex from the command line using the `dorsal-ronflex` command. The command takes a path to an ABF file or a directory containing ABF files as its main argument:

```sh
dorsal-ronflex path/to/your/abf/files
```

### Options

- `-o`, `--output`: Specifies the path to the output directory. By default, the output is saved in the current directory.

```sh
dorsal-ronflex path/to/your/abf/files -o path/to/output/directory
```

- `-c`, `--config`: Specifies the path to a configuration file. The configuration file is a JSON file that can be used to customize various aspects of the analysis. If no configuration file is provided, the program uses default settings.

```sh
dorsal-ronflex path/to/your/abf/files -c path/to/config.json
```

## Configuration

The configuration file is a JSON file that can contain the following keys:

- `segment_start`: The start of the segment.
- `segment_end`: The end of the segment.
- `default_curve_check`: The default curve check value.
- `default_ms_delay`: The default millisecond delay.
- `default_tolerance`: The default tolerance.
- `default_abs_tolerance`: The default absolute tolerance.
- `default_channel`: The default channel.

Here is an example of a configuration file:

```json
{
    "segment_start": 5568,
    "segment_end": 5668,
    "default_curve_check": 90,
    "default_ms_delay": 5,
    "default_tolerance": 0.1,
    "default_abs_tolerance": 0.14,
    "default_channel": 1
}
```

You can find an example configuration file in the `docs/` directory: `docs/example_config.json`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

Dorsal Ronflex is licensed under the MIT license.