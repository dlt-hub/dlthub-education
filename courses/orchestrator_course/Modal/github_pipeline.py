import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_source

config: RESTAPIConfig = {
    "client": {
        "base_url": "https://api.github.com",
        "auth": {
            "token": dlt.secrets["sources.access_token"],
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
                    "initial_value": "2025-03-01T00:00:00Z",
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
                "incremental": {
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

# Only run the pipeline if this script is executed directly
if __name__ == "__main__":
    print("Starting pipeline setup...")
    pipeline = dlt.pipeline(
            pipeline_name="github_repos_issues",
            destination="duckdb",
            dataset_name="github_data",
            progress="log"  # Add logging as per rule recommendation
        )

    load_info = pipeline.run(github_source)

    print("Pipeline run complete.")
    print(pipeline.last_trace)