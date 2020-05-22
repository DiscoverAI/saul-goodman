# Saul Goodman
Pipeline orchestration to create a working drug creation model.

## Install
```bash
pipenv install && pipenv run airflow initdb
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
