# MLOps Final Project

This project demonstrates the implementation of MLOps principles using various tools and technologies. The main features include CI/CD orchestration, data version control with DVC and Yandex Object Bucket Storage, and Docker containerization.

## Technologies 

- DVC: For data version control and synchronization with remote storage.
- GitHub Actions: For CI/CD pipeline automation.
- Docker: For creating containerized applications.
- FastAPI: For building the API server.
- Yandex Cloud: For remote bucket data storage.

## CI/CD Pipeline

The CI/CD pipeline is set up using GitHub Actions. It includes the following steps:

1. Checkout repository: Clones the repository.
2. Set up Python: Sets up the Python environment.
3. Install dependencies: Installs required packages.
4. Run tests: Executes unit and data quality tests.
5. Build Docker image: Builds the Docker image.
6. Push Docker image: Pushes the Docker image to Docker Hub with unic github.sha.

GitHub Actions Configuration
The GitHub Actions workflow is defined in .github/workflows/ci-cd.yml.

# Setup Instructions

## Prerequisites
- Docker
- Python 3.8+
- Git
- DVC

## Clone repo 

```bash
git clone https://github.com/your-username/MLOps_final.git
cd MLOps_final
```

Also all docker images available on https://hub.docker.com/repository/docker/vskolegov/mlops_final/general

## Setting Up DVC

```bash
dvc remote add -d myremote s3://your-yandex-bucket-storage-name/path/to/dvcstore
dvc remote modify myremote endpointurl https://storage.yandexcloud.net
dvc remote modify myremote access_key_id your_access_key_id
dvc remote modify myremote secret_access_key your_secret_access_key
```
Replace placeholders like your-username, your-bucket, your_access_key_id, and your_secret_access_key with the actual values for your setup.

your_access_key_id and your_secret_access_key is a service account tokens


## Build and Run the Docker Image

```bash
docker build -t mlops_final:latest .
docker run -p 8000:8000 mlops_final:latest
```
FastAPI server now started at http://localhost:8000/docs

## Running Unit and Data Quality Tests
The CI/CD pipeline is configured to run tests automatically. However, you can also run tests locally using pytest.

# Yandex Cloud 

### Install Yandex Cloud CLI

```bash
iex (New-Object System.Net.WebClient).DownloadString('https://storage.yandexcloud.net/yandexcloud-yc/install.ps1')
```
https://yandex.cloud/ru/docs/cli/quickstart

- Create yc token.
- Create Bucket Object Storage
- When prompted by the command, enter the OAuth token you received earlier
```bash
yc init
```
- Choice folder (cloud) and server to use, paste token
- Create service account with roles: storage.admin and viwer
- Generate pair of static keys:

```bash
yc iam access-key create --service-account-id $SERVICE_ACCOUNT_ID
```
Use keys in GitHub Actions (service account)

### dvc support
Also for S3 API support
```bash
pip install dvc[s3]
```

Now you can configure dvc using yandex bucket object storage.

My object storage for this project: https://storage.yandexcloud.net/vskolegov-dvc

# API Endpoints

- /predict/: Endpoint for making predictions.
- /retrain/: Endpoint for retraining the model with new data.

# Links

1. Docker Hub
https://hub.docker.com/repository/docker/vskolegov/mlops_final/general

3. Yandex Object Storage
https://storage.yandexcloud.net/vskolegov-dvc