# Rapidly developing ELT pipelines with dltHub and Dagster

## Project Goal
Integrate a dlt pipeline with Dagster using the Dagster-dlt integration, running the pipeline in parallel mode. This project demonstrates how to orchestrate multiple dlt resources in parallel from Dagster using the `dagster_dlt` integration.

- **Processing Mode:** Parallel
- **Integration:** Dagster-dlt integration (`dagster_dlt`, `dlt_assets`)



## Run the Notebook Demo (Colab)

You can follow along with the first part of the project directly in a hosted notebook:

 **[Open the Colab notebook →](https://colab.research.google.com/drive/1XDVlaS2WzD1TKgsZOHOw9tEvNFPOmIzV?usp=sharing)**

This notebook covers:
- Creating a `dlt` pipeline using the Jaffle Shop API
- Loading data into DuckDB
- Inspecting the resulting tables

The remaining integration and orchestration steps are demonstrated **live** or via local development.

---

## Step-by-Step Instructions


## Step 1: Install dlt and Dagster

### Install dlt and dependencies

Go to the project folder:
```shell
cd workshops/deep_dive_dagster/dlt-dagster-integration-parallel-pipeline
```
Install dependencies from `pyproject.toml`:

```shell
uv sync
```

or
```shell
uv add "dlt[bigquery,duckdb]" pandas
```

### Install Dagster

You don't have to install Dagster, just use `uv`.

[Install Dagster with uv](https://docs.dagster.io/getting-started/installation).


## Step 2: Install the `dagster-dlt` integration

[Official documentation for dagster_dlt integration](https://docs.dagster.io/guides/build/components/integrations/dlt-component-tutorial).

Add the `dagster-dlt` library to the project (it's actually already installed through `uv sync`):

```shell
uv add dagster-dlt
```

The dlt-Dagster integration allows you to use dlt (Data Load Tool) to easily ingest and replicate data between systems through Dagster.

### What is dlt?

[Data Load Tool (dlt)](https://dlthub.com/) is an open source library for creating efficient data pipelines. It offers features like secret management, data structure conversion, incremental updates, and pre-built sources and destinations, simplifying the process of loading messy data into well-structured datasets.

### How the integration works

The Dagster dlt integration uses multi-assets, where a single definition results in [multiple assets](https://docs.dagster.io/integrations/libraries/dlt/using-dlt-with-dagster). These assets are derived from the DltSource, and each dlt resource maps to Dagster assets.

### Key components

The integration requires two main components:
1. **dlt source**: Defines how to extract data from external systems.
2. **dlt pipeline**: Specifies how the data should be loaded into your destination.

## Step 3: Define the pipeline and assets

### dlt Source

In this demo we create dlt source for [Jaffle Shop REST API](https://jaffle-shop.scalevector.ai/docs) using [REST API dlt source](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic).

Location:`dlt_dagster_integration_parallel_pipeline/defs/jaffle_shop_source.py`


### Assets
- In Dagster, `assets.py` is typically a Python module where you define your software-defined assets using the `@asset` decorator (`@dlt_assets` in our case). 
- Assets represent data that your pipelines produce and consume, and Dagster models them as first-class objects rather than just tasks.
- An asset definition is a description, in code, of an asset that should exist and how to produce and update that asset.

Location: `dlt_dagster_integration_parallel_pipeline/defs/assets.py`

### Definitions

- The definitions.py file contains a Definitions object that acts like a project manifest for Dagster - it bundles together all the assets, jobs, schedules, sensors, and resources that make up your Dagster project
- This allows Dagster to know exactly what's available to run in your specific project.
- The Definitions object essentially tells Dagster: "Here's everything that's available to run in this project"

Location: `dlt_dagster_integration_parallel_pipeline/definitions.py`

## Step 4: Test it locally
At this point, you can list the Dagster definitions in your project with `dg list defs`. You should see the asset you just created:

```shell
uv run dg list defs
```
You can also load and validate your Dagster definitions with `dg check defs`:
```shell
uv run dg check defs
```

## Step 5: Run the pipeline
In the terminal, navigate to your project's root directory and run:
```shell
uv run dg dev
```
Open your web browser and navigate to http://localhost:3000, where you should see the Dagster UI.

1. In the top navigation, click **Assets > View lineage**.

2. Click **Materialize** to run the pipeline.

3. In the popup or **Runs**, click **View**. This will open the **Run** details page, allowing you to view the run as it executes. Use the view buttons in near the top left corner of the page to change how the run is displayed. You can also click the asset to view logs and metadata.

## Deploy on Dagster+
The easiest way to deploy your Dagster project is to use Dagster+.

Check out the [Dagster+ documentation](https://docs.dagster.io/dagster-plus/) to learn more.
