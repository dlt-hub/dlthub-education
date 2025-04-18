import dlt
from dlt.sources.helpers import requests

BASE_URL = "https://api.github.com/repos/dlt-hub/dlt"

def pagination(url):
    while True:
        response = requests.get(url)
        response.raise_for_status()
        yield response.json()

        # Get next page
        if "next" not in response.links:
            break
        url = response.links["next"]["url"]

@dlt.resource(
    table_name="issues",
    write_disposition="merge",
    primary_key="id",
)
def get_issues(
        updated_at=dlt.sources.incremental("updated_at", initial_value="1970-01-01T00:00:00Z")
):
    url = (
        f"{BASE_URL}/issues?since={updated_at.last_value}&per_page=100&sort=updated"
        "&directions=desc&state=open"
    )
    yield pagination(url)

@dlt.resource(
    table_name="pull_requests",
    write_disposition="merge",
    primary_key="id",
)
def get_pulls(
        updated_at=dlt.sources.incremental("updated_at", initial_value="1970-01-01T00:00:00Z")
):
    url = (
        f"{BASE_URL}/pulls?since={updated_at.last_value}&per_page=100&sort=updated"
        "&directions=desc&state=open"
    )
    yield pagination(url)

@dlt.source
def github_source():
    return get_issues()


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_issues_merge",
        destination="duckdb",
        dataset_name="github_data_merge",
    )

    load_info = pipeline.run(github_source())
    print(pipeline.last_trace.last_normalize_info)
    print(load_info)