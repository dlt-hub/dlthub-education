# Build Portable Data Lake with OSS

## Create a dlt pipeline 

For this example we load GitHub issues from dlt-hub repository to local filesystem as parquet files.

```shell
python load_data_to_fylesystem.py
```

All your data will be processed, typed, unnested and loaded in `bucket_url="./data_lake"`.

## Connect to schema with Ibis

```shell

pip install -U "ibis-framework[duckdb]"

```

Use Ibis to read parquet files like:
```py
 # Read the Parquet files into an Ibis table
table = ibis.read_parquet(item["file_url"])
```

Use dlt to load transformed data into Warehouse (DuckDB), run the command:
```shell
python read_tables_ibis.py
```

Use `dlt pipeline` command to see your transformed data in DuckDB:

```shell
dlt pipeline github_data_lake_ibis show
```

## Connect to schema with duckdb

Use DuckDB to read parquet files like:

```sql
SELECT * FROM read_parquet('{item["file_url"][7:]}')
```

Use dlt to load transformed data into Warehouse, run the command:
```shell
python read_tables_duckdb.py
```

References:
- https://duckdb.org/2021/06/25/querying-parquet
- https://motherduck.com/blog/duckdb-dbt-e2e-data-engineering-project-part-2/


## Create dbt models
1. Install dbt and Set Up a Project

If you haven’t installed dbt yet, you can install it using pip:
```shell
pip install dbt-core
pip install dbt-duckdb # or dbt-postgres, dbt-bigquery, etc.
```

To initialize a new dbt project, run:

```
dbt init github_issues_project
```
This will create a new folder structure for your project.

2. Define the GitHub Issues Data Source
In your `models/` directory, create a new file called `github_issues.yml` to define your GitHub Issues source. For example, if the data is in a table called github_issues, your source configuration could look like this:

```yaml
version: 2
sources:
  - name: github_raw
    tables:
      - name: issues
```

Ensure that this matches the actual name of the table in your warehouse.


3. Create a Model for Transformations
Next, create a SQL model in the models/ folder that will define how you want to transform the raw GitHub Issues data. For example, let’s create a model that aggregates the number of open issues per repository:

Create a new file called open_issues_by_repo.sql:

```sql
WITH raw_issues AS (
    SELECT *
    FROM {{ source('github_raw', 'issues') }}
)
SELECT 
    COUNT(*) AS open_issues
FROM raw_issues
WHERE state = 'open'
```

4. Configure dbt Profiles
Make sure your dbt profile is configured to point to your data warehouse. The profiles.yml file will typically look like this:

```yaml
github_issues_project:
  target: dev
  outputs:
    dev:
      type: {your-warehouse}  # postgres, bigquery, redshift, etc.
      host: {your-host}
      user: {your-username}
      password: {your-password}
      dbname: {your-database}
      schema: {your-schema}
      threads: 1
```

5. Run the dbt Model
To run the model, execute the following command:
```shell
dbt run
```

This will execute the SQL in the open_issues_by_repo.sql model, transforming your raw GitHub Issues data into an aggregated table.