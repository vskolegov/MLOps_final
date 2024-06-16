# Get start

## Yandex Cloud

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
- Choice folder (cloud) and server to use
- Create service account and generate pair of static keys

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


# Links
## Docker Hub
https://hub.docker.com/repository/docker/vskolegov/mlops_final/general
## Datasets

https://drive.google.com/drive/folders/1F4idC9MZvpW43vZtrgubh-iC6vFitCkj?usp=sharing

