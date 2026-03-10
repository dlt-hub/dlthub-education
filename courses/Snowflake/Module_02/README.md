# Module 2: Running dlt Inside Snowflake with Snowpark Container Services

## Introduction

In Module 2, you learned to use S3 as external staging for faster Snowflake loads. Now, we'll take it a step further by running the entire dlt pipeline **inside Snowflake** using Snowpark Container Services (SPCS).

**Why run dlt inside Snowflake?**
- **Cost Efficient**: SPCS containers cost ~6% of the smallest warehouse
- **No External Infrastructure**: No need to deploy to AWS Lambda, Airflow, or other orchestration tools
- **Native Orchestration**: Trigger pipelines using Snowflake Tasks
- **Secure**: Credentials never leave Snowflake
- **Elastic**: Auto-suspend and resume based on schedule

**Reference:** [Can you run dlt inside Snowflake? (Part 2/2: SPCS)](https://www.sfrt.io/can-you-run-dlt-inside-snowflake-part-2-2-spcs/)

---

## Prerequisites

Before starting, ensure you have:

1. **Python 3.11+** and **dlt** installed in your virtual environment
2. **Docker Desktop** installed and running
3. **Snowflake account** with `ADMIN` privileges
4. **Completed Module 01**
   - Working dlt pipeline with external staging (S3)
   - `DLT_LOADER_ROLE` configured

---

## Step 1: Prepare Your dlt Pipeline for Containerization

### 1.1 Update Your Pipeline Script

Update `github_api_pipeline.py` — change the `pipeline_name` and `dataset_name` (around line 58-62):

**From:**
```python
pipeline = dlt.pipeline(
    pipeline_name="github_stg_api_pipeline",
    destination='snowflake',
    staging="filesystem",
    dataset_name="github_stg_api_data",
    progress="log",
)
```

**To:**
```python
pipeline = dlt.pipeline(
    pipeline_name="github_api_spcs_pipeline",
    destination='snowflake',
    staging="filesystem",
    dataset_name="github_spcs_data",
    progress="log",
)
```

### 1.2 Verify Your requirements.txt

Your `requirements.txt` should only contain what runs in the container:

```txt
dlt[snowflake,s3]>=1.23.0
```

**Note:** Do NOT add `snowflake-cli-labs` here - it's only needed on your local machine, not in the container.

### 1.3 Verify Your Configuration Files

Your `.dlt/secrets.toml`:

```toml
access_token = "ghp_your_github_token"

[destination.snowflake.credentials]
database = "DLT_DATA"
password = "your_password"
username = "YOUR_USERNAME"
host = "YOUR_ACCOUNT_IDENTIFIER"
warehouse = "COMPUTE_WH"
role = "DLT_LOADER_ROLE"

[destination.filesystem.credentials]
aws_access_key_id = "YOUR_AWS_ACCESS_KEY"
aws_secret_access_key = "YOUR_AWS_SECRET_KEY"

[destination.filesystem]
bucket_url = "s3://gtm-demos/snowflake-demo/"
```

Your `.dlt/config.toml` — add the `[destination.snowflake]` section if not already present:

```toml
[runtime]
log_level = "WARNING"
dlthub_telemetry = true

[destination.snowflake]
truncate_tables_on_staging_destination_before_load = true
```

### 1.4 Test Locally First

Before containerizing, test the pipeline:

```bash
python github_api_pipeline.py
```

Ensure it runs successfully!

---

## Step 2: Install Snowflake CLI in Your Virtual Environment

Since you're managing everything in your virtual environment:

```bash
# Make sure your virtual environment is activated
# You should see (your-venv-name) in your prompt

# Install Snowflake CLI in your virtual env
pip install snowflake-cli-labs

# Verify installation
snow --version
```

---

## Step 3: Create Docker Container

### 3.1 Create Dockerfile

Create a file named `Dockerfile` (no extension) in your project root:

```dockerfile
FROM python:3.11-slim

# Set Python to run in unbuffered mode so logs appear immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy all project files
COPY ./ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# When container launches, run the pipeline script
CMD ["python", "-u", "github_api_pipeline.py"]
```

### 3.2 Create .dockerignore

Create `.dockerignore` to exclude unnecessary files:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.log
.git/
.gitignore
*.md
.DS_Store
.venv/
```

### 3.3 Create SPCS Service Specification

Create `load-github.yaml`:

```yaml
spec:
  containers:
    - name: load-github
      image: kgiotue-wn98412.registry.snowflakecomputing.com/dlt_data/github_dlt_spcs/image_repo/load_github:latest
```

---

## Step 4: Set Up Snowflake Infrastructure

### 4.1 Create Schema and Image Repository

Run in Snowflake (Snowsight or SnowSQL):

```sql
USE ROLE ACCOUNTADMIN;

-- Create schema for SPCS resources
CREATE SCHEMA IF NOT EXISTS DLT_DATA.GITHUB_DLT_SPCS;

-- Create image repository to store Docker images
CREATE IMAGE REPOSITORY IF NOT EXISTS DLT_DATA.GITHUB_DLT_SPCS.IMAGE_REPO;

-- Grant permissions to your role
GRANT READ, WRITE ON IMAGE REPOSITORY DLT_DATA.GITHUB_DLT_SPCS.IMAGE_REPO
TO ROLE DLT_LOADER_ROLE;

-- View repository details
SHOW IMAGE REPOSITORIES IN SCHEMA DLT_DATA.GITHUB_DLT_SPCS;
```

### 4.2 Create Stage for Service Specifications

```sql
USE ROLE DLT_LOADER_ROLE;

-- Create stage to hold service YAML files
CREATE STAGE IF NOT EXISTS DLT_DATA.GITHUB_DLT_SPCS.SPEC_STAGE
DIRECTORY = (ENABLE = TRUE AUTO_REFRESH = TRUE);

-- Verify stage
SHOW STAGES IN SCHEMA DLT_DATA.GITHUB_DLT_SPCS;
```

### 4.3 Create Compute Pool

```sql
USE ROLE ACCOUNTADMIN;

-- Create compute pool for running containers
CREATE COMPUTE POOL IF NOT EXISTS CP_DLT_PIPELINE
MIN_NODES = 1
MAX_NODES = 1
INSTANCE_FAMILY = CPU_X64_XS
AUTO_RESUME = TRUE
AUTO_SUSPEND_SECS = 60;

-- Grant permissions
GRANT USAGE, MONITOR, OPERATE ON COMPUTE POOL CP_DLT_PIPELINE
TO ROLE DLT_LOADER_ROLE;

-- Check compute pool status
SHOW COMPUTE POOLS;
```

### 4.4 Create External Access Integration

This allows your container to access GitHub API, AWS S3, and Snowflake.

**Step 1: Get Snowflake Endpoints**

```sql
USE ROLE ACCOUNTADMIN;

-- Get Snowflake endpoints for network rule
SELECT LISTAGG(
    CONCAT('''', value:host::STRING, ':', value:port::NUMBER, ''''),
    ', '
)
FROM TABLE(FLATTEN(INPUT => PARSE_JSON(SYSTEM$ALLOWLIST())));
```

**Copy the output** - you'll need it in the next step.

**Step 2: Create Network Rules**

```sql
USE ROLE ACCOUNTADMIN;

-- Network rule for GitHub API
CREATE OR REPLACE NETWORK RULE DLT_DATA.GITHUB_DLT_SPCS.NR_GITHUB
MODE = 'EGRESS'
TYPE = 'HOST_PORT'
VALUE_LIST = ('api.github.com:443');

-- Network rule for AWS S3 (EU region)
CREATE OR REPLACE NETWORK RULE DLT_DATA.GITHUB_DLT_SPCS.NR_S3
MODE = 'EGRESS'
TYPE = 'HOST_PORT'
VALUE_LIST = (
    's3.amazonaws.com:443',
    's3.eu-central-1.amazonaws.com:443',
    'gtm-demos.s3.amazonaws.com:443',
    'gtm-demos.s3.eu-central-1.amazonaws.com:443'
);

-- Network rule for Snowflake (paste output from previous query)
CREATE OR REPLACE NETWORK RULE DLT_DATA.GITHUB_DLT_SPCS.NR_SNOWFLAKE
MODE = 'EGRESS'
TYPE = 'HOST_PORT'
VALUE_LIST = (
    -- Paste the comma-separated list from SYSTEM$ALLOWLIST() query here
    -- Example: 'abc123.snowflakecomputing.com:443', 'xyz789.snowflakecomputing.com:443'
);

-- Network rule for dlt telemetry (optional)
CREATE OR REPLACE NETWORK RULE DLT_DATA.GITHUB_DLT_SPCS.NR_DLT_TELEMETRY
MODE = 'EGRESS'
TYPE = 'HOST_PORT'
VALUE_LIST = ('telemetry.scalevector.ai:443');
```

**Step 3: Create External Access Integration**

```sql
USE ROLE ACCOUNTADMIN;

-- Create external access integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION EAI_GITHUB_DLT
ALLOWED_NETWORK_RULES = (
    DLT_DATA.GITHUB_DLT_SPCS.NR_GITHUB,
    DLT_DATA.GITHUB_DLT_SPCS.NR_S3,
    DLT_DATA.GITHUB_DLT_SPCS.NR_SNOWFLAKE,
    DLT_DATA.GITHUB_DLT_SPCS.NR_DLT_TELEMETRY
)
ENABLED = TRUE;

-- Grant permissions
GRANT USAGE ON INTEGRATION EAI_GITHUB_DLT TO ROLE DLT_LOADER_ROLE;
```

---

## Step 5: Build and Push Docker Image

### 5.1 Ensure Docker Desktop is Running

Make sure Docker Desktop is running (you should see the whale icon in your menu bar).

### 5.2 Build Docker Image

In your terminal (from project directory, with virtual env activated):

```bash
# Build image for linux/amd64 (Snowflake SPCS platform)
docker build --platform=linux/amd64 -t github-pipeline:latest .
```

**Expected output:**
```
[+] Building 45.2s (9/9) FINISHED
Successfully tagged github-pipeline:latest
```

### 5.3 Tag Image for Snowflake

```bash
# Tag with your Snowflake registry path
docker tag github-pipeline:latest \
  kgiotue-wn98412.registry.snowflakecomputing.com/dlt_data/github_dlt_spcs/image_repo/load_github:latest
```

### 5.4 Configure Snowflake CLI Connection

First, check your Snowflake account details:

```sql
-- Run in Snowflake to get account identifier
SELECT CURRENT_ACCOUNT();

-- Get region
SELECT CURRENT_REGION();
```

Then create the Snowflake CLI configuration:

```bash
# Create config directory
mkdir -p ~/.snowflake

# Create config file (use single quotes for password with special characters)
cat > ~/.snowflake/config.toml << 'EOF'
[connections.default]
account = "***********"
user = "*******"
password = "your_password_here"
role = "DLT_LOADER_ROLE"
warehouse = "COMPUTE_WH"
database = "DLT_DATA"
schema = "GITHUB_DLT_SPCS"
EOF

# Set secure permissions
chmod 0600 ~/.snowflake/config.toml
```

**Important:**
- Replace the password with your actual password
- Use single quotes to handle special characters in password

### 5.5 Test Snowflake CLI Connection

```bash
# Test the connection
snow connection test
```

**Expected output:**
```
+----------------------------------------------------------+
| key             | value                                  |
|-----------------+----------------------------------------|
| Connection name | default                                |
| Status          | OK                                     |
| Account         | ***************                        |
| User            | ********                               |
+----------------------------------------------------------+
```

### 5.6 Login to Snowflake Registry

```bash
# Login using Snowflake CLI
snow spcs image-registry login
```

### 5.7 Push Image to Snowflake

```bash
# Push image to Snowflake registry
docker push kgiotue-wn98412.registry.snowflakecomputing.com/dlt_data/github_dlt_spcs/image_repo/load_github:latest
```

**Expected output:**
```
The push refers to repository [kgiotue-wn98412.registry.snowflakecomputing.com/dlt_data/github_dlt_spcs/image_repo/load_github]
latest: digest: sha256:abc123... size: 1234
```

### 5.8 Upload Service Specification to Snowflake

**Option A: Via Snowsight UI**
1. Go to Data → Databases → DLT_DATA → GITHUB_DLT_SPCS → Stages → SPEC_STAGE
2. Click "+ Files"
3. Upload `load-github.yaml`

**Option B: Via SQL**
```sql
PUT file:///Users/shreyas/Desktop/SPCS_DEMO/load-github.yaml
@DLT_DATA.GITHUB_DLT_SPCS.SPEC_STAGE
AUTO_COMPRESS=FALSE
OVERWRITE=TRUE;
```

**Option C: Via Snowflake CLI**
```bash
snow stage copy load-github.yaml @DLT_DATA.GITHUB_DLT_SPCS.SPEC_STAGE --overwrite
```

---

## Step 6: Run Your Pipeline in SPCS

### 6.1 Execute Job Service

```sql
USE ROLE DLT_LOADER_ROLE;
USE WAREHOUSE COMPUTE_WH;

-- Execute the containerized pipeline
EXECUTE JOB SERVICE
IN COMPUTE POOL CP_DLT_PIPELINE
NAME = DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB
EXTERNAL_ACCESS_INTEGRATIONS = (EAI_GITHUB_DLT)
FROM @DLT_DATA.GITHUB_DLT_SPCS.SPEC_STAGE
SPECIFICATION_FILE = 'load-github.yaml';
```

**Important:** Parameter order matters! Compute pool first, then other params, specification last.

### 6.2 Monitor Job Execution

Wait 1-2 minutes, then check status:

```sql
-- Check job status
CALL SYSTEM$GET_JOB_STATUS('DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB');
```

**Expected output:**
```
Job JOB_LOAD_GITHUB completed successfully with status: DONE.
```

### 6.3 View Job Logs

```sql
-- View container logs
CALL SYSTEM$GET_SERVICE_LOGS(
    'DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB',
    '0',
    'load-github',
    100
);
```

---

## Step 7: Verify Everything Works

### 7.1 Check Loaded Data

```sql
USE DATABASE DLT_DATA;
USE SCHEMA GITHUB_SPCS_DATA;

-- View all tables
SHOW TABLES IN SCHEMA GITHUB_SPCS_DATA;

-- Check repos data
SELECT COUNT(*) AS total_repos FROM GITHUB_SPCS_DATA.REPOS;

SELECT
    NAME,
    FULL_NAME,
    STARGAZERS_COUNT,
    _DLT_LOAD_ID
FROM GITHUB_SPCS_DATA.REPOS
ORDER BY STARGAZERS_COUNT DESC
LIMIT 10;

-- Check issues data
SELECT COUNT(*) AS total_issues FROM GITHUB_SPCS_DATA.ISSUES;

SELECT
    TITLE,
    STATE,
    UPDATED_AT,
    _DLT_LOAD_ID
FROM GITHUB_SPCS_DATA.ISSUES
ORDER BY UPDATED_AT DESC
LIMIT 10;
```

### 7.2 Check Load History

```sql
-- View load metadata
SELECT
    LOAD_ID,
    SCHEMA_NAME,
    STATUS,
    INSERTED_AT,
    SCHEMA_VERSION_HASH
FROM GITHUB_SPCS_DATA._DLT_LOADS
ORDER BY INSERTED_AT DESC;
```

The `INSERTED_AT` timestamp should show when the SPCS job ran!

### 7.3 Check S3 Staging Files

```bash
python view_s3_staging.py
```

You should see files in the `snowflake-demo/github_spcs_data/` folder.

---

## Step 8: Run Again to Test Reliability

To verify the pipeline is reliable:

```sql
USE ROLE DLT_LOADER_ROLE;

-- Drop the existing job service
DROP SERVICE DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB;

-- Execute again
EXECUTE JOB SERVICE
IN COMPUTE POOL CP_DLT_PIPELINE
NAME = DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB
EXTERNAL_ACCESS_INTEGRATIONS = (EAI_GITHUB_DLT)
FROM @DLT_DATA.GITHUB_DLT_SPCS.SPEC_STAGE
SPECIFICATION_FILE = 'load-github.yaml';
```

Check load history again - you should see multiple loads:

```sql
SELECT
    LOAD_ID,
    SCHEMA_NAME,
    STATUS,
    INSERTED_AT
FROM GITHUB_SPCS_DATA._DLT_LOADS
ORDER BY INSERTED_AT DESC
LIMIT 5;
```

---

## Step 9: Schedule Pipeline with Snowflake Tasks (Optional)

### 9.1 Create Scheduled Task

```sql
USE ROLE DLT_LOADER_ROLE;

-- Create task to run pipeline every hour
CREATE OR REPLACE TASK DLT_DATA.GITHUB_DLT_SPCS.TASK_LOAD_GITHUB
WAREHOUSE = COMPUTE_WH
SCHEDULE = 'USING CRON 0 * * * * UTC'  -- Every hour at minute 0
AS
EXECUTE JOB SERVICE
IN COMPUTE POOL CP_DLT_PIPELINE
NAME = DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB_SCHEDULED
EXTERNAL_ACCESS_INTEGRATIONS = (EAI_GITHUB_DLT)
FROM @DLT_DATA.GITHUB_DLT_SPCS.SPEC_STAGE
SPECIFICATION_FILE = 'load-github.yaml';

-- Activate the task
ALTER TASK DLT_DATA.GITHUB_DLT_SPCS.TASK_LOAD_GITHUB RESUME;
```

### 9.2 Manage Task

```sql
-- View task details
SHOW TASKS IN SCHEMA DLT_DATA.GITHUB_DLT_SPCS;

-- Pause task
ALTER TASK DLT_DATA.GITHUB_DLT_SPCS.TASK_LOAD_GITHUB SUSPEND;

-- Resume task
ALTER TASK DLT_DATA.GITHUB_DLT_SPCS.TASK_LOAD_GITHUB RESUME;

-- View task run history
SELECT *
FROM TABLE(DLT_DATA.INFORMATION_SCHEMA.TASK_HISTORY(
    TASK_NAME => 'TASK_LOAD_GITHUB',
    SCHEDULED_TIME_RANGE_START => DATEADD('day', -7, CURRENT_TIMESTAMP())
))
ORDER BY SCHEDULED_TIME DESC;
```

---

## Troubleshooting

### Issue: Docker Build Fails

**Check:**
- Is Docker Desktop running?
- Are you in the correct directory with `Dockerfile`?

### Issue: Snowflake CLI Connection Fails

**Check:**
- Is your account identifier correct?
- Is your password correct? (use single quotes for special characters)
- Do you have network access to Snowflake?

**Common Error:** "Could not connect to Snowflake backend"
- Run `SELECT CURRENT_ACCOUNT();` and `SELECT CURRENT_REGION();` in Snowflake
- Use the account locator without region suffix in config

### Issue: Job Fails with Network Error

**Check logs:**
```sql
CALL SYSTEM$GET_SERVICE_LOGS('DLT_DATA.GITHUB_DLT_SPCS.JOB_LOAD_GITHUB', '0', 'load-github', 100);
```

**Common fixes:**
- Missing S3 regional endpoint in network rules (e.g., `s3.eu-central-1.amazonaws.com:443`)
- Missing GitHub API endpoint
- Wrong bucket name or region

### Issue: Image Repository Not Found

**Verify:**
```sql
SHOW IMAGE REPOSITORIES IN SCHEMA DLT_DATA.GITHUB_DLT_SPCS;
```

Make sure the image path in `load-github.yaml` matches the actual repository.

---

## Cost Optimization

### Auto-Suspend Strategy

```sql
-- Aggressive auto-suspend (60 seconds)
ALTER COMPUTE POOL CP_DLT_PIPELINE
SET AUTO_SUSPEND_SECS = 60;

-- Check current settings
SHOW COMPUTE POOLS LIKE 'CP_DLT_PIPELINE';
```

---

## Key Takeaways

- **No External Infrastructure**: Pipeline runs entirely within Snowflake
- **Cost Efficient**: SPCS containers are cost efficient
- **Native Scheduling**: Use Snowflake Tasks for orchestration
- **Secure**: Credentials managed by Snowflake
- **S3 Staging Still Works**: Container can use external S3 staging
- **Elastic**: Auto-suspend and resume based on schedule

---

## Summary of What You Built

```
┌─────────────────────────────────────────┐
│   Snowflake SPCS Container              │
│   ┌─────────────────────────────┐       │
│   │  Your dlt Pipeline          │       │
│   │  (Docker Image)             │       │
│   └─────────────────────────────┘       │
│            ↓                             │
│     Extract from GitHub API              │
│            ↓                             │
│     Stage files in S3 (EU)               │
│            ↓                             │
│     Load into Snowflake                  │
└─────────────────────────────────────────┘
       Triggered by Snowflake Task
```

**Data Flow:**
1. SPCS container starts on compute pool
2. dlt extracts data from GitHub API
3. Files staged in S3 (eu-central-1)
4. Snowflake loads from S3 using COPY INTO
5. Container auto-suspends after completion
