Sign Up or Login to modal.com

Download and configure the Python client
Run this in order to install the Python library locally:

```
pip install modal
python3 -m modal setup
```

The first command will install the Modal client library on your computer, along with its dependencies.

The second command creates an API token by authenticating through your web browser. It will open a new tab, but you can close it when you are done.

follow the instructions in quick Start

Add dlt and github source to requirements: https://modal.com/docs/examples/webscraper#add-dependencies

```py
dlt_image = modal.Image.debian_slim(python_version="3.12").run_commands(
    "apt-get update",
    'pip install "dlt[bigquery]"',
).add_local_python_source("github_pipeline")
```


### Credentials

Secrets are attached directly to functions:
```py
@app.function(
    image=dlt_image,
    secrets=[modal.Secret.from_name("github-api")]
)
def run_pipeline(resource):
    ...
```

### Run locally
```shell
modal run github_pipeline_modal.py
```

### Backfilling
```shell
modal run github_pipeline_modal_backfill.py --start-date '2025-08-01 05:47:07+00:00' --end-date '2025-09-01 05:47:07+00:00'
```

### Deploy 
```shell
modal deploy --name github_scheduled github_pipeline_modal.py
```

### Deploy in parallel

```shell
modal deploy --name github_scheduled_parallel github_pipeline_modal_parallel.py
```