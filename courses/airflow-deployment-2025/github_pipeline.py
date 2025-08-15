import dlt
from dlt.sources.rest_api import rest_api_source
import os

# limit for number of pages - very conservative to avoid rate limits
RESOURCE_LIMIT = 2

# GitHub API configuration
REPO_OWNER = "dlt-hub"
REPO_NAME = "dlt"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"


# Define the github source - this will be used by the DAG
github_source = rest_api_source(
    {
        "client": {
            "base_url": BASE_URL,
            "auth": {"token": dlt.secrets.get("sources.github_pipeline.github_source.github_token", "")}
        },
        "resource_defaults": {
            "endpoint": {
                "params": {
                    "per_page": 100,
                },
            },
        },
        "resources": [
            {
                "name": "issues",
                "endpoint": {
                    "path": "/issues",
                    "params": {
                        "state": "all",
                        "sort": "updated",
                        "direction": "desc"
                    }
                },
                "write_disposition": "merge",
                "primary_key": "id"
            },
            {
                "name": "pulls",
                "endpoint": {
                    "path": "/pulls",
                    "params": {
                        "state": "all",
                        "sort": "updated",
                        "direction": "desc"
                    }
                },
                "write_disposition": "merge",
                "primary_key": "id"
            },
            {
                "name": "commits",
                "endpoint": {
                    "path": "/commits",
                    "params": {
                        "per_page": 100
                    }
                },
                "write_disposition": "merge",
                "primary_key": "sha"
            },
            {
                "name": "releases",
                "endpoint": {
                    "path": "/releases"
                },
                "write_disposition": "merge",
                "primary_key": "id"
            },
            {
                "name": "contributors",
                "endpoint": {
                    "path": "/contributors",
                    "params": {
                        "anon": "false"
                    }
                },
                "write_disposition": "merge",
                "primary_key": "id"
            }
        ],
    }
)




# add limit to number of pages collected for each endpoint
github_source.issues.add_limit(RESOURCE_LIMIT)
github_source.pulls.add_limit(RESOURCE_LIMIT)
github_source.commits.add_limit(RESOURCE_LIMIT)
github_source.releases.add_limit(RESOURCE_LIMIT)
github_source.contributors.add_limit(RESOURCE_LIMIT)

# Only run the pipeline if this script is executed directly
if __name__ == "__main__":
    print("Starting GitHub pipeline setup...")
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_github",
        destination="bigquery",
        dataset_name="github_dataset",
        progress="log"
    )
    print("Pipeline created.")
    print("GitHub source created.")

    load_info = pipeline.run(github_source)
    print("Pipeline run complete.")
    print("Load info:", load_info)
