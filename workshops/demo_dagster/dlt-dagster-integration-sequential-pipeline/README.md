# dlt_dagster_integration_sequential_pipeline

## Project Goal
Integrate a DLT pipeline with Dagster using the Dagster-DLT integration, running the pipeline in sequential mode. This project demonstrates how to orchestrate a DLT pipeline from Dagster using the `dagster_dlt` integration.

- **Processing Mode:** Sequential
- **Integration:** Dagster-DLT integration (`dagster_dlt`, `dlt_assets`)

## Getting Started

Install your Dagster code location as a Python package (in editable mode):

```bash
pip install -e ".[dev]"
```

Start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

## Installation for Building the Dagster Graph

The following commands were used to build the Dagster graph/codebase. You can use either `pip` or [`uv`](https://github.com/astral-sh/uv) for faster installs:

```bash
# With pip
pip install dagster dagster-embedded-elt
pip install "dlt[bigquery]"

# Or with uv (recommended for speed)
uv pip install dagster dagster-embedded-elt
uv pip install "dlt[bigquery]"
```

To scaffold a new Dagster project (if starting from scratch):

```bash
dagster project scaffold --name <your-project-name>
```

> **Note:** These commands are for building the codebase and setting up the project structure. For running the project, see the instructions below.

## Assets
- Main assets are defined in `dlt_dagster_integration_sequential_pipeline/assets.py`.

## Development

### Adding new Python dependencies
Specify new Python dependencies in `setup.py`.

### Unit Testing
Tests are in the `dlt_dagster_integration_sequential_pipeline_tests` directory. Run tests using:

```bash
pytest dlt_dagster_integration_sequential_pipeline_tests
```

### Schedules and Sensors
If you want to enable Dagster [Schedules](https://docs.dagster.io/guides/automate/schedules/) or [Sensors](https://docs.dagster.io/guides/automate/sensors/) for your jobs, the [Dagster Daemon](https://docs.dagster.io/guides/deploy/execution/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

## Deploy on Dagster+
The easiest way to deploy your Dagster project is to use Dagster+.

Check out the [Dagster+ documentation](https://docs.dagster.io/dagster-plus/) to learn more.
