# Robotiive

Unofficial script for running Robotiive tasks.

> **Important:** Robotiive does not have any official documentation for its API. The functionality in this tool was reverse-engineered by studying [Execute_robotiive](https://github.com/calvin44/Execute_robotiive) and then rewritten to be more maintainable and user-friendly.

## Installation

Ensure you have Python 3.12+ installed.

Install the `robotiive` package using either `pip` or `uv`. We recommend `uv` for better performance.

> Note: This tool is typically installed globally, but you can use a virtual environment if preferred.

### Using `pip`

Install directly from the GitHub repository:
```sh
pip install git+https://github.com/Stanley5249/robotiive.git
```

### Using `uv`

1. Install `uv` by following the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

2. Install the package as a tool:
```sh
uv tool install git+https://github.com/Stanley5249/robotiive.git
```

Learn more about UV tools [here](https://docs.astral.sh/uv/concepts/tools/).

## Usage

**Important:** Ensure the Robotiive software is running before using these commands.

### Run a Specific Task

Execute a single task within a project:
```sh
robotiive run <project_name> <task_name>
```

### Run All Tasks

Execute all tasks in a project sequentially:
```sh
robotiive run-all <project_name>
```

## License

This project is licensed under the MIT License.