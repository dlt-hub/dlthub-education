from prefect import flow, task
import dlt


@task(log_prints=True)
def run_pipeline():

    import github_pipeline

    source = github_pipeline.github_source

    pipeline = dlt.pipeline(
        pipeline_name="github_pipeline",
        destination="bigquery",
        dataset_name="demo_github",
        progress="log"
    )

    info = pipeline.run(source)
    print(info)
    return info

@flow(log_prints=True)
def main():

    github_workflow = run_pipeline()
    return github_workflow

if __name__ == "__main__":
    main.serve(name="my-first-deployment")