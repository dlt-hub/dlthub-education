import dlt
import github_pipeline

def main():

    #load the source from our github_pipeline module
    source = github_pipeline.github_source

    #initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name="orchestra_github_init",
        destination="bigquery",
        dataset_name="orchestra_github_init",
        progress="log"
    )

    #run pipeline
    info = pipeline.run(source)

    print("Pipeline finished:")
    print(info)
    return info

if __name__ == "__main__":
    main()