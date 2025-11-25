import dlt
import os
import github_pipeline


def run_resource(
    resource_name: str, start_date: str | None = None, end_date: str | None = None
):
    base_source = github_pipeline.github_source

    # apply incremental only if explicitly passed
    if start_date is not None and end_date is not None:
        # dynamically get the resource
        resource = getattr(base_source, resource_name)
        resource.apply_hints(
            incremental=dlt.sources.incremental(
                "created_at",
                initial_value=start_date,
                end_value=end_date,
                row_order="asc",
            )
        )

    selected_source = base_source.with_resources(resource_name)

    # initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name=f"orchestra_github_bck_{resource_name}",
        destination="bigquery",
        dataset_name="orchestra_github_bck",
        progress="log",
    )

    info = pipeline.run(selected_source)
    print(f"{resource_name} -> {info}")
    return info


def main():

    start_date = os.environ.get("START_DATE")
    end_date = os.environ.get("END_DATE")

    a = run_resource("repos")
    b = run_resource("releases")
    c = run_resource("forks", start_date=start_date, end_date=end_date)

    return a, b, c


if __name__ == "__main__":
    main()
