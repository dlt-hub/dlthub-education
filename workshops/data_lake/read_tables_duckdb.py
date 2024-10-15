import duckdb
import dlt
from dlt.sources.filesystem import filesystem


@dlt.source()
def transform_data():
    # Connect to DuckDB (can be in-memory or to a file)
    con = duckdb.connect()
    # Define the path to your Parquet files
    raw_data_lake = '/Users/alena/dlthub/dlthub-education/workshops/data_lake/data_lake/github_raw'

    filesystem_issues = filesystem(
        bucket_url=raw_data_lake + "/issues/",
        file_glob="**/*.parquet"
    )

    @dlt.transformer(data_from=filesystem_issues)
    def transform_issues(items):
        for item in items:
            print(item)
            # Read the Parquet file into DuckDB
            issue_counts_df = con.execute(
                f"""
                    WITH parquet_data AS (
                        SELECT * 
                        FROM read_parquet('{item["file_url"][7:]}') 
                        WHERE state = 'open'
                    )
                    SELECT
                        user__login,
                        COUNT(*) AS issue_count
                    FROM parquet_data
                    GROUP BY user__login;
                """
            ).df()
            yield issue_counts_df

    return transform_issues


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_data_lake_duckdb",
        destination="duckdb",
        dataset_name="github_transformed_duckdb",
    )

    load_info = pipeline.run(transform_data())
    print(pipeline.last_trace.last_normalize_info)
    print(load_info)



