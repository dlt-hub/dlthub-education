import os

import dlt
from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets

from .dagster_pipeline import github_source  # import the right source

initial_value = os.getenv("ISSUES_INITIAL_VALUE")

# replace hardcoded incremental loading parameters in issues endpoint
github_source.issues.apply_hints(
    incremental=dlt.sources.incremental(
        cursor_path="updated_at",
        initial_value=initial_value,
    )
)

# replace hardcoded backfilling parameters in forks endpoint
forks_initial_value = os.getenv("FORKS_INITIAL_VALUE", "")
forks_end_value = os.getenv("FORKS_END_VALUE", "")

if forks_initial_value and forks_end_value:  # only apply if both env vars are set
    github_source.forks.apply_hints(
        incremental=dlt.sources.incremental(
            cursor_path="updated_at",
            initial_value=forks_initial_value,
            end_value=forks_end_value,
            row_order="asc",
        )
    )


def make_resource_asset(resource_name: str):
    @dlt_assets(
        dlt_source=github_source.with_resources(
            resource_name
        ),  # use the correct source
        dlt_pipeline=dlt.pipeline(
            pipeline_name=f"github_dagster_pipeline_{resource_name}",
            dataset_name="github_dagster_dataset",
            destination="bigquery",  # use the right destination
            progress="log",
        ),
        name=f"github_{resource_name}",
        group_name="github",
    )
    def dagster_github_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
        yield from dlt.run(context=context)

    return dagster_github_assets


resource_names = ["repos", "contributors", "issues", "forks", "releases"]
dagster_github_assets_parallel = [
    make_resource_asset(resource) for resource in resource_names
]
