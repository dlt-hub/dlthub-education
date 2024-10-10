# Build Data Lake with dlt, Ibis and dbt

## Create a dlt pipeline 

For this example we load GitHub issues from dlt-hub repository to local filesystem as parquet files.

```shell
python load_data_to_fylesystem.py
```

All you data will be processed, typed, unnested and loaded in `bucket_url="./data_lake".
`
## Connect to schema with Ibis

```shell

pip install -U "ibis-framework[duckdb]"

```

## Connect to schema with duckdb

https://motherduck.com/blog/duckdb-dbt-e2e-data-engineering-project-part-2/

## Create dbt models

