# Airflow Deployment with dlt - Pokemon Pipeline

This course demonstrates how to deploy dlt pipelines using Apache Airflow 2.x.

## 🎯 What You'll Learn

- Setting up Apache Airflow 2.x locally
- Creating dlt pipelines for data extraction
- Deploying dlt pipelines as Airflow DAGs
- Configuring BigQuery as a destination
- Running parallel vs sequential pipeline processing

## 📁 Project Structure

```
airflow-deployment-2025/
├── dags/
│   ├── pokemon_pipeline.py          # dlt pipeline definition
│   ├── dag_rest_api_pokemon.py      # Sequential DAG
│   └── dag_rest_api_pokemon_parallel.py  # Parallel DAG
├── chess_pipeline.py                 # Additional pipeline example
├── requirements.txt                  # Python dependencies
├── secrets.toml.template            # Credentials template
└── README.md                        # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Google Cloud Project with BigQuery enabled
- Service account with BigQuery permissions

### 2. Setup Virtual Environment

```bash
python -m venv air_venv
source air_venv/bin/activate  # On Windows: air_venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Credentials

**Option A: Using .dlt/secrets.toml**
```bash
# Copy the template and fill in your credentials
cp secrets.toml.template .dlt/secrets.toml
# Edit .dlt/secrets.toml with your actual credentials
```

**Option B: Using Airflow Variables**
```bash
# Set Airflow variables for BigQuery credentials
airflow variables set bigquery_project_id "your-project-id"
airflow variables set bigquery_client_email "your-service-account@your-project.iam.gserviceaccount.com"
airflow variables set bigquery_private_key "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----"
```

### 4. Start Airflow

```bash
export AIRFLOW_HOME="$(pwd)"
airflow standalone
```

### 5. Access Airflow Web UI

- URL: http://localhost:8080
- Username: `admin`
- Password: Check terminal output for the generated password

## 🔧 DAGs Overview

### Pokemon DAGs

1. **`pokemon_dag`** (Sequential Processing)
   - Uses `decompose="serialize"`
   - Processes data sequentially
   - Good for smaller datasets

2. **`pokemon_dag_parallel`** (Parallel Processing)
   - Uses `decompose="parallel-isolated"`
   - Processes data in parallel with separate pipeline instances
   - Better for larger datasets

### Pipeline Features

- **Source**: Pokemon REST API
- **Destination**: BigQuery
- **Schedule**: Daily (`@daily`)
- **Error Handling**: Built-in retry mechanisms

## 🔐 Security Notes

⚠️ **Important**: Never commit actual credentials to version control!

- The `secrets.toml.template` file shows the structure without real credentials
- Use environment variables or Airflow variables for production deployments
- Consider using Google Secret Manager for production environments

## 📊 Monitoring

### Check DAG Status
```bash
# List all DAG runs
airflow dags list-runs -d pokemon_dag

# Check running tasks
airflow tasks list -d pokemon_dag --state running

# View DAG details
airflow dags show pokemon_dag
```

### Common Issues

1. **"ModuleNotFoundError: No module named 'dlt'"**
   - Ensure virtual environment is activated
   - Install dlt: `pip install dlt[bigquery]`

2. **"Variable bigquery_project_id does not exist"**
   - Set required Airflow variables (see step 3)

3. **BigQuery authentication errors**
   - Verify service account permissions
   - Check credentials format in secrets file

## 🎓 Learning Objectives

By the end of this course, you'll be able to:

- ✅ Deploy dlt pipelines to Apache Airflow
- ✅ Configure BigQuery as a destination
- ✅ Understand sequential vs parallel processing
- ✅ Monitor and troubleshoot Airflow DAGs
- ✅ Implement proper credential management

## 📚 Additional Resources

- [dlt Documentation](https://dlthub.com/docs)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Google BigQuery Documentation](https://cloud.google.com/bigquery/docs)

## 🤝 Contributing

This is part of the dlt-hub education repository. Feel free to submit issues or pull requests!