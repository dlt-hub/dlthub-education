import dlt
import os
import github_pipeline

def run_resource(resource_name: str):
    base_source = github_pipeline.github_source

    selected_source = base_source.with_resources(resource_name)

    #initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name=f"orchestra_github_parallel_{resource_name}",
        destination="bigquery",
        dataset_name=f"orchestra_github_parallel_{resource_name}",
        progress="log"
    )

    info = pipeline.run(selected_source)
    print(f"{resource_name} -> {info}")
    return info

def main():
    resource_name = os.environ["RESOURCE_NAME"]
    return run_resource(resource_name)

if __name__ == "__main__":
    main()
    


    