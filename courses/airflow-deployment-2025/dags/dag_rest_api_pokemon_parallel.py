from datetime import timedelta
from airflow.decorators import dag

import dlt
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup
from airflow.models import Variable
import os

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
    dag_id="pokemon_dag_parallel",
    schedule_interval='@daily',
    start_date=pendulum.datetime(2023, 7, 1),
    catchup=False,
    max_active_runs=1,  # Keep this at 1 to avoid multiple DAG runs
    default_args=default_task_args,
    concurrency=10  # Allow up to 10 tasks to run in parallel (more aggressive)
)
def load_data_parallel():

    # Set environment variables inside the DAG function to avoid import timeouts
    # Fetch Airflow variables and set as env vars with correct dlt naming convention for the parallel pipeline
    os.environ["REST_API_POKEMON_PARALLEL__DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID"] = Variable.get("bigquery_project_id")
    os.environ["REST_API_POKEMON_PARALLEL__DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL"] = Variable.get("bigquery_client_email")

    # Fix private key formatting - replace literal \n with actual newlines (private key has \n in it)
    private_key = Variable.get("bigquery_private_key").replace("\\n", "\n")
    os.environ["REST_API_POKEMON_PARALLEL__DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY"] = private_key

    # Also set the fallback environment variables that dlt looks for
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID"] = Variable.get("bigquery_project_id")
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL"] = Variable.get("bigquery_client_email")
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY"] = private_key

    # set `use_data_folder` to True to store temporary data on the `data` bucket. Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup("pipeline_parallel", use_data_folder=False, wipe_local_data=True)

    # Import the source function from pokemon_pipeline.py
    from pokemon_pipeline import pokemon_source

    # modify the pipeline parameters 
    pipeline = dlt.pipeline(
        pipeline_name='rest_api_pokemon_parallel',
        dataset_name='pokemon_dataset_parallel',
        destination="bigquery",
        full_refresh=False, # Keep incremental loading
        dev_mode=False # Disable dev mode to enable decomposition
    )
    
    # create the source, using "parallel-isolated" for true parallelization
    # This creates separate pipeline instances for each resource, avoiding BigQuery timing conflicts
    # All resources will still use the same dataset name, creating one database with all tables
    tasks.add_run(
        pipeline,
        pokemon_source,
        decompose="parallel-isolated",  # Separate pipelines avoid BigQuery timing issues
        trigger_rule="all_done",
        retries=0,
        provide_context=True
    )

dag = load_data_parallel()

# run: export AIRFLOW_HOME="/Users/dlthubgtm/Desktop/Aashish/Airflow Sandbox" 