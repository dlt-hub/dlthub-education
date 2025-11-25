import dlt
import github_pipeline


def run_resource(resource_name: str):
    base_source = github_pipeline.github_source

    selected_source = base_source.with_resources(resource_name)

    # initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name=f"orchestra_github_dynamic_{resource_name}",
        destination="bigquery",
        dataset_name="orchestra_github_dynamic",
        progress="log",
    )

    info = pipeline.run(selected_source)
    print(f"{resource_name} -> {info}")
    return info


def main():
    a = run_resource("repos")
    b = run_resource("releases")
    c = run_resource("issues")

    return a, b, c


if __name__ == "__main__":
    main()
