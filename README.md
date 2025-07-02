# DLT Demo Pipeline for the GA4 Admin API

## Prerequisites for Getting Started

A code editor (e.g., [VS Code](https://code.visualstudio.com/download)): You will need a suitable code editor for writing and managing your code.

[uv](https://docs.astral.sh/uv/getting-started/installation/) as a fast Python package manager (installation): Install uv to efficiently manage your Python packages.

[Google Cloud Project](https://developers.google.com/workspace/guides/create-project): It is highly recommended to create a new Google Cloud Project to avoid overwriting existing configurations or data in your current projects. Ensure that GCP billing is enabled for this new project.

gcloud command-line tool (installation): Install the [gcloud](https://cloud.google.com/sdk/docs/install) command-line interface for interacting with Google Cloud services.

## How to run this locally?

```bash
uv venv
source .venv/bin/activate
uv sync
```

```bash
gcloud auth login
```

```bash
export GCP_PROJECT="your-gcp-project-id-here"
gcloud config set project $GCP_PROJECT
gcloud services enable analyticsadmin.googleapis.com
gcloud auth application-default login --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/analytics.readonly"
```

Be aware this runs in all projects that you have access to with your account!

```bash
uv run pipeline.py
```

## How to deploy this on Google Cloud?

After trying this out locally you can also deploy this to the cloud. With the project defined above.

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

```bash
export SERVICE_ACCOUNT_NAME="cloud-run-ga4"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
 --description="Service account for Cloud Run to Import Data in Bigquery"
```

```bash
gcloud projects add-iam-policy-binding ${GCP_PROJECT} \
--member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com" \
--role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
--member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
--member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/bigquery.readSessionUser"

print "${SERVICE_ACCOUNT_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com"
```

Give the service account printed above the permissions to acces you GA4 Accounts relevant.

```bash
gcloud run jobs deploy ga4-admin-pipeline \
  --source . \
  --tasks 1 \
  --max-retries 3 \
  --region europe-west3 \
  --project=$GCP_PROJECT \
  --service-account="${SERVICE_ACCOUNT_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com"
```
