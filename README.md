# Saul Goodman
> "Congratulations! You're Now Officially The Cute One Of The Group."
>
> -- Saul Goodman (Breaking Bad)

Pipeline orchestration to create a working drug creation model.

For more information please check out the [SARS-CoV-2 project](https://github.com/DiscoverAI/sars-cov-2-drug-design).

## Install
```bash
pipenv install && pipenv run airflow initdb
```

## Test
### Test DAGs
```bash
pipenv run test-dag
```

## Start Webserver
```bash
pipenv run start-server
```

## Start Scheduler
```bash
pipenv run start-scheduler
```

## Setup airflow
To make the airflow DAG files work, you have to setup `aws` and `emr` connections.
The [aws connection](https://airflow.apache.org/docs/stable/howto/connection/aws.html) name should be `aws_default` and
the emr connection name should be `emr_default`.

## Config
Following environment variables are needed:
```bash
DATALAKE=s3://<s3 bucket>
MLFLOW_TRACKING_URI=<url of mlflow instance>
PINKMAN_JAR_URI=<s3 url of the pinkman jar to use>
PINKMAN_LOG_URI=<s3 location for storing logs>
COMPUTE_ENVIRONMENT_JOB_QUEUE=<ARN of the aws compute environment>
WALTER_WHITE_JOB_DEFINITION=<ARN of the aws batch job definition for walter white>
```
