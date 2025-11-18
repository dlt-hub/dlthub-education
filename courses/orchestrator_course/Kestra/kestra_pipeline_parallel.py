import argparse
import os

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_source

config: RESTAPIConfig = {
    "client": {
        "base_url": "https://api.github.com",
        "auth": {
            "token": os.getenv("SOURCES__ACCESS_TOKEN"),
        },
        "headers": {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        "paginator": "header_link",
    },
    "resources": [
        {
            "name": "repos",
            "endpoint": {"path": "orgs/dlt-hub/repos"},
        },
        {
            "name": "contributors",
            "endpoint": {
                "path": "repos/dlt-hub/dlt/contributors",
            },
        },
        {
            "name": "issues",
            "endpoint": {
                "path": "repos/dlt-hub/dlt/issues",
                "params": {
                    "state": "open",  # Only get open issues
                    "sort": "updated",
                    "direction": "desc",
                    "since": "{incremental.start_value}",  # For incremental loading
                },
                "incremental": {
                    "cursor_path": "updated_at",
                    "initial_value": "2025-07-01T00:00:00Z",
                },
            },
        },
        {
            "name": "forks",
            "endpoint": {
                "path": "repos/dlt-hub/dlt/forks",
                "params": {
                    "sort": "oldest",  # Ensures ascending creation order
                    "per_page": 100,
                },
                "incremental": {  # backfill
                    "cursor_path": "created_at",
                    "initial_value": "2025-07-01T00:00:00Z",
                    "row_order": "asc",
                },
            },
        },
        {
            "name": "releases",
            "endpoint": {
                "path": "repos/dlt-hub/dlt/releases",
            },
        },
    ],
}

github_source = rest_api_source(config)

# dynamic incremental loading (issues)
initial_value = os.getenv("ISSUES_INITIAL_VALUE")

github_source.issues.apply_hints(
    incremental=dlt.sources.incremental(
        cursor_path="updated_at",
        initial_value=initial_value,
    )
)


# dynamic backfilling (forks)
forks_initial_value = os.getenv("FORKS_INITIAL_VALUE", "")
forks_end_value = os.getenv("FORKS_end_VALUE", "")

if forks_initial_value and forks_end_value:
    github_source.forks.apply_hints(
        incremental=dlt.sources.incremental(
            cursor_path="created_at",
            initial_value=forks_initial_value,
            end_value=forks_end_value,
            row_order="asc",
        )
    )

# create the resource flag
ap = argparse.ArgumentParser()
ap.add_argument(
    "--resource",
    required=True,
    choices=["repos", "contributors", "issues", "forks", "releases"],
)
args = ap.parse_args()


# omit unwanted endpoints from source config
github_source = github_source.with_resources(args.resource)

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_pipeline_kestra",
        destination="bigquery",
        dataset_name="github_data_kestra_parallel",
        progress="log",  # Add logging as per rule recommendation
    )

    load_info = pipeline.run(github_source)
    print(load_info)
