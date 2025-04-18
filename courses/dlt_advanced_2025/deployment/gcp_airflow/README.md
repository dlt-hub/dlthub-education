# Airflow

Apache Airflow is an open-source platform used to programmatically author, schedule, and monitor workflows. It allows users to define complex workflows as directed acyclic graphs (DAGs) of tasks, where each task represents a unit of work.

Google Cloud Composer is a managed Apache Airflow service that allows you to orchestrate your workflows across cloud and on-premises environments. This guide will walk you through the steps to run a Python script as an Airflow DAG in Google Cloud Composer.

## Prerequisites

1. **Google Cloud Account**: Ensure you have a Google Cloud account and billing is set up.
2. **Google Cloud Composer Environment**: Create or have access to an existing Cloud Composer environment.
3. **Basic knowledge of Airflow**: Familiarity with Airflow concepts like DAGs, tasks, and operators.


## Step 1. Install dlt

First you need to add additional dependencies that `deploy` command requires:

```python
pip install "dlt[cli]"
```

## Step 2. Create dlt pipeline

**Note**: That dlt Airflow helper works only with dlt source. Your resources always should be grouped in a source.

```python
import dlt
from dlt.sources.helpers import requests

...

@dlt.source
def github_source():
    return get_issues()

pipeline = dlt.pipeline(
    pipeline_name="github_issues_merge",
    destination="duckdb",
    dataset_name="github_data_merge",
)

load_info = pipeline.run(github_source())
print(pipeline.last_trace.last_normalize_info)
print(load_info)
```

## Step 3. Ensure your pipeline works

Before you can deploy, you must run your pipeline locally at least once.

```sh
python github_source.py 
```

This should successfully load data from the source to the destination once and allows `dlt` to gather required information for the deployment.

```sh
**❯ python github_source.py** 
Normalized data for the following tables:
- _dlt_pipeline_state: 1 row(s)
- issues: 177 row(s)
- issues__labels: 128 row(s)
- issues__assignees: 82 row(s)
- issues__performed_via_github_app__events: 25 row(s)

Load package 1724177356.448274 is NORMALIZED and NOT YET LOADED to the destination and contains no failed jobs
Pipeline github_issues_merge load step completed in 2.14 seconds
1 load package(s) were loaded to destination duckdb and into dataset github_data_merge
The duckdb destination used duckdb:////Users/alena/dlthub/dlthub-education/workshops/workshop-august-2024/part2/deployment/gcp_airflow/github_issues_merge.duckdb location to store data
Load package 1724177356.448274 is LOADED and contains no failed jobs
```

## Step 4. Run deploy command

```sh
dlt deploy github_source.py airflow-composer
```

This command checks if your pipeline has run successfully before and creates the following folders:

- build
    - This folder contains a file called `cloudbuild.yaml` with a simple configuration for cloud deployment. We will use it below.
- dags
    - This folder contains the Python script `dag_{pipeline_name}.py`, which is an example of a simple serialized DAG using the Airflow *PipelineTasksGroup* wrapper.
    
    **Note:** This folder is only needed to store DAG scripts, but it is not the Airflow *dags_folder*. Please refer to the [Troubleshooting](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-airflow-composer#troubleshooting) section for more information.
    

By default, the `dlt deploy` command shows you the deployment credentials in ENV format.

💡 When you run the dlt deploy command, you will get the relevant info in your CLI about how you can deploy credentials.

```sh
❯ **dlt deploy github_source.py airflow-composer**
Looking up the deployment template scripts in https://github.com/dlt-hub/dlt-deploy-template.git...

Your airflow-composer deployment for pipeline github_issues_merge is ready!
* The airflow cloudbuild.yaml file was created in build.
* The dag_github_issues_merge.py script was created in dags.

You must prepare your DAG first:
1. Import your sources in dag_github_issues_merge.py, configure the DAG ans tasks as needed.
2. Test the DAG with Airflow locally .
See Airflow getting started: https://airflow.apache.org/docs/apache-airflow/stable/start.html

If you are planning run the pipeline with Google Cloud Composer, follow the next instructions:

1. Read this doc and set up the Environment: https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-airflow-composer
2. Set _BUCKET_NAME up in build/cloudbuild.yaml file. 
3. Your pipeline does not seem to need any secrets.
4. Add dlt package below using Google Composer UI.
dlt[duckdb]>=0.5.3
NOTE: You may need to add more packages ie. when your source requires additional dependencies
5. Commit and push the pipeline files to github:
a. Add stage deployment files to commit. Use your Git UI or the following command
git add ../../../../../dags/dag_github_issues_merge.py ../../../../../build/cloudbuild.yaml
b. Commit the files above. Use your Git UI or the following command
git commit -m 'initiate github_issues_merge pipeline with Airflow'
WARNING: You have modified files in your repository. Do not forget to push changes to your pipeline script as well!
c. Push changes to github. Use your Git UI or the following command
git push origin
6. You should see your pipeline in Airflow.
```

## Step 5. Modify DAG

In directory `dags/` you can find the file `dag_github_issues_merge.py` that you need to edit. It has the following structure:

```python
from datetime import timedelta
from airflow.decorators import dag

import dlt
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup

# modify the default task arguments - all the tasks created for dlt pipeline will inherit it
# - set e-mail notifications
# - we set retries to 0 and recommend to use `PipelineTasksGroup` retry policies with tenacity library, you can also retry just extract and load steps
# - execution_timeout is set to 20 hours, tasks running longer that that will be terminated

default_task_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': 'test@test.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'execution_timeout': timedelta(hours=20),
}

# modify the default DAG arguments
# - the schedule below sets the pipeline to `@daily` be run each day after midnight, you can use crontab expression instead
# - start_date - a date from which to generate backfill runs
# - catchup is False which means that the daily runs from `start_date` will not be run, set to True to enable backfill
# - max_active_runs - how many dag runs to perform in parallel. you should always start with 1

@dag(
    schedule_interval='@daily',
    start_date=pendulum.datetime(2023, 7, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args
)
def load_data():
    # set `use_data_folder` to True to store temporary data on the `data` bucket. Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup("pipeline_decomposed", use_data_folder=False, wipe_local_data=True)

    # import your source from pipeline script
    from pipeline_or_source_script import source

    # modify the pipeline parameters 
    pipeline = dlt.pipeline(pipeline_name='pipeline_name',
                     dataset_name='dataset_name',
                     destination='duckdb',
                     full_refresh=False # must be false if we decompose
                     )
    # create the source, the "serialize" decompose option will converts dlt resources into Airflow tasks. use "none" to disable it
    tasks.add_run(pipeline, source(), decompose="serialize", trigger_rule="all_done", retries=0, provide_context=True)

load_data()
```

1. First, we should import sources from our existing pipeline script `github_source` as:

```python
from workshops.workshop_august_2024.part2.deployment.gcp_airflow import github_source
```

1. Then we pass the pipeline instance and source instance to the `add_run` method of tasks.

```python
tasks.add_run(pipeline, github_source(), decompose="serialize", trigger_rule="all_done", retries=0, provide_context=True)
```

## Step 6. Test locally

1. Install Airflow
    
    https://airflow.apache.org/docs/apache-airflow/stable/start.html
    
2. Change Airflow home directory to run DAG from your project folder.
    
    ```python
    export AIRFLOW__CORE__DAGS_FOLDER=/Users/alena/dlthub/dlthub-education
    ```
    
3. Run Airflow Standalone:
    
    The `airflow standalone` command initializes the database, creates a user, and starts all components.
    
    ```python
    airflow standalone
    ```
    
4. Access the Airflow UI:
    
    Visit `localhost:8080` in your browser and log in with the admin account details shown in the terminal.
    
    ```python
    standalone | Airflow is ready
    standalone | Login with username: admin  password: k34hsd1ig38f9YPu4ao9e
    standalone | Airflow Standalone is for development purposes only. Do not use this in production!
    ```
    

## Step 7. Or Run it in Google Cloud Composer

### 1. [**Google Cloud Composer setup**](https://dlthub.com/docs/reference/explainers/airflow-gcp-cloud-composer)

### 2. [**Deploy a pipeline with Airflow and Google Composer**](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-airflow-composer)
