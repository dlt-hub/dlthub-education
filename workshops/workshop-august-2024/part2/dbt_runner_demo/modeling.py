import dlt

if __name__ == "__main__":
    # perform transformations on the data loaded by dlt
    pipeline = dlt.pipeline(
        pipeline_name='github_issues_merge',
        destination='duckdb',
        dataset_name='modeled_issues'
    )

    # get venv for dbt
    venv = dlt.dbt.get_venv(pipeline)

    # get runner
    dbt = dlt.dbt.package(
        pipeline,
        "workshop_demo",
        venv=venv
    )

    # run the dbt models
    models = dbt.run_all()

    for m in models:
        print(
            f"Model {m.model_name} materialized" +
            f"in {m.time}" +
            f"with status {m.status}" +
            f"and message {m.message}"
        )