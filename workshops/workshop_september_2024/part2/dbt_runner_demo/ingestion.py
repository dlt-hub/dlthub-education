import dlt
from dlt.sources.helpers import requests

BASE_URL = "https://api.github.com/repos/dlt-hub/dlt/issues"


def pagination(url):
    while True:
        response = requests.get(url)
        response.raise_for_status()
        yield response.json()

        # Get next page
        if "next" not in response.links:
            break
        url = response.links["next"]["url"]


if __name__ == "__main__":
    @dlt.resource(
        table_name="issues",
        write_disposition="merge",
        primary_key="id",
    )
    def get_issues(
        updated_at=dlt.sources.incremental("updated_at", initial_value="2024-01-01T00:00:00Z")
    ):
        url = (
            f"{BASE_URL}?since={updated_at.last_value}&per_page=100&sort=updated"
            "&directions=desc&state=open"
        )
        yield pagination(url)


    pipeline = dlt.pipeline(
        pipeline_name="github_issues_merge",
        destination="duckdb",
        dataset_name="github_data_merge",
    )
    load_info = pipeline.run(get_issues)
    print(load_info)