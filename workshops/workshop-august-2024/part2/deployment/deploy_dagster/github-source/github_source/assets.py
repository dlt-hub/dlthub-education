
from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline
from .github_resources import github_source


@dlt_assets(
    dlt_source=github_source(),
    dlt_pipeline=pipeline(
        pipeline_name="github_issues",
        dataset_name="github",
        destination="duckdb",
    ),
    name="github",
    group_name="github",
)
def dagster_github_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
