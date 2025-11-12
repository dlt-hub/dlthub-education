import argparse
import os
import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_source

# --- your existing config ---
config: RESTAPIConfig = {
    "client": {
        "base_url": "https://api.github.com",
        "auth": {
            "token": os.getenv("SOURCES__ACCESS_TOKEN"),
        },
        "headers": {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        },
        "paginator": "header_link",
    },
    "resources": [
        {"name": "repos", "endpoint": {"path": "orgs/dlt-hub/repos"}},
        {"name": "contributors", "endpoint": {"path": "repos/dlt-hub/dlt/contributors"}},
        {
            "name": "issues",
            "endpoint": {
                "path": "repos/dlt-hub/dlt/issues",
                "params": {
                    "state": "open",
                    "sort": "updated",
                    "direction": "desc",
                    "since": "{incremental.start_value}",
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
                "params": {"sort": "oldest", "per_page": 100},
                "incremental": {
                    "cursor_path": "created_at",
                    "initial_value": "2025-07-01T00:00:00Z",
                    "row_order": "asc",
                },
            },
        },
        {"name": "releases", "endpoint": {"path": "repos/dlt-hub/dlt/releases"}},
    ],
}

github_source = rest_api_source(config)

# --- CLI flag for selecting a single resource ---
ap = argparse.ArgumentParser()
ap.add_argument(
    "--resource",
    required=True,
    choices=["repos", "contributors", "issues", "forks", "releases"],
    help="Which resource to run via with_resources()",
)
args = ap.parse_args()

# --- run just the selected resource ---
source = github_source.with_resources(args.resource)

pipeline = dlt.pipeline(
    pipeline_name=f"github_pipeline_kestra_{args.resource}",
    destination="bigquery",
    dataset_name="github_data_kestra_parallel",
    progress="log",
)

print(f"[Kestra] Starting resource: {args.resource}")
load_info = pipeline.run(source)
print(load_info)
