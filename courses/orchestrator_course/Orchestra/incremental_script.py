import dlt
import os
import github_pipeline


def run_resource(resource_name: str, incremental_date: str | None = None):
    base_source = github_pipeline.github_source

    # apply incremental only if explicitly passed
    if incremental_date is not None:
        # dynamically get the resource
        resource = getattr(base_source, resource_name)
        resource.apply_hints(
            incremental=dlt.sources.incremental(
                "updated_at",
                initial_value=incremental_date,
            )
        )

    selected_source = base_source.with_resources(resource_name)

    # initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name=f"orchestra_github_inc_{resource_name}",
        destination="bigquery",
        dataset_name="orchestra_github_inc",
        progress="log",
    )

    info = pipeline.run(selected_source)
    print(f"{resource_name} -> {info}")
    return info


def main():

    incremental_date = os.environ.get("INCREMENTAL_DATE")

    a = run_resource("repos")
    b = run_resource("releases")
    c = run_resource("issues", incremental_date=incremental_date)

    return a, b, c


if __name__ == "__main__":
    main()
