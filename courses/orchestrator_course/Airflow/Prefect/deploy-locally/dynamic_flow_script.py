from prefect import flow, task
import dlt


@task(log_prints=True)
def run_resource(resource_name: str):

    import github_pipeline

    source = github_pipeline.github_source.with_resources(resource_name)

    pipeline = dlt.pipeline(
        pipeline_name=f"github_dynamic_{resource_name}",
        destination="bigquery",
        dataset_name="demo_dynamic_github",
        progress="log"
    )

    info = pipeline.run(source)
    print(f"{resource_name} -> {info}")
    return info

@flow(log_prints=True)
def main():

    a = run_resource("repos")
    b = run_resource("contributors")
    c = run_resource("releases")

    return a, b, c

if __name__ == "__main__":
    main.serve(name="dynamic-deployment")