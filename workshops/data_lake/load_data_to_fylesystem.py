
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
    write_disposition="replace",
    table_format="delta",
)
def get_issues():
    url = (
        f"{BASE_URL}/issues?per_page=100&sort=updated"
        "&directions=desc&state=open"
    )
    yield pagination(url)


@dlt.source
def github_source():
    return get_issues()


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_data_lake_raw",
        destination="filesystem",
        dataset_name="github_raw",
    )

    load_info = pipeline.run(github_source(), loader_file_format="parquet")
    print(pipeline.last_trace.last_normalize_info)
    print(load_info)