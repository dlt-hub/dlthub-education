import os
import ibis
import dlt
from dlt.sources.filesystem import filesystem


@dlt.source()
def transform_data():
    # Define the path to your Parquet files
    raw_data_lake = 'file://Users/alena/dlthub/dlthub-education/workshops/data_lake/data_lake/github_raw'

    filesystem_issues = filesystem(
        bucket_url=raw_data_lake + "/issues/",
        file_glob="**/*.parquet"
    )

    @dlt.transformer(data_from=filesystem_issues)
    def transform_issues(items):
        for item in items:
            # Read the Parquet files into an Ibis table
            table = ibis.read_parquet(item["file_url"])

            open_issues = table.filter(table.state == 'open')
            open_issues_df = open_issues.execute()
            print("Open Issues:\n", open_issues_df.columns)

            issue_counts = open_issues.group_by('user__login').count()
            issue_counts_df = issue_counts.execute()
            print("Issues Count by User:\n", issue_counts_df)

            yield issue_counts_df

    return transform_issues


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_data_lake_ibis",
        destination="duckdb",
        dataset_name="github_transformed_ibis",
    )

    load_info = pipeline.run(transform_data())
    print(pipeline.last_trace.last_normalize_info)
    print(load_info)



