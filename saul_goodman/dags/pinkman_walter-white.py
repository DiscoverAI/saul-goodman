import os
from datetime import timedelta

from airflow import DAG
from airflow.contrib.operators.awsbatch_operator import AWSBatchOperator
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.sensors.emr_job_flow_sensor import EmrJobFlowSensor
from airflow.utils.dates import days_ago

PINKMAN_SPARK_STEPS = [
    {
        'Name': 'pinkman',
        'ActionOnFailure': 'TERMINATE_CLUSTER',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode',
                'cluster',
                '--master',
                'yarn',
                '--class',
                'com.github.discoverai.pinkman.Pinkman',
                os.getenv("PINKMAN_JAR_URI"),
                os.getenv("DATALAKE").replace("s3://", ""),
                os.getenv("MLFLOW_TRACKING_URI")
            ]
        }
    }
]
PINKMAN_JOB_FLOW_OVERRIDES = {
    'Name': 'Pinkman',
    'ReleaseLabel': 'emr-6.0.0',
    "LogUri": os.getenv("PINKMAN_LOG_URI"),
    'Instances': {
        "Ec2KeyName": "tuco-key",
        'InstanceGroups': [
            {
                'Name': 'Master nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm4.large',
                'InstanceCount': 1,
            },
            {
                'Name': 'Core nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': 'm4.large',
                'InstanceCount': 4,
            }
        ],
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False,
    },
    'Steps': PINKMAN_SPARK_STEPS,
    'Applications': [
        {'Name': 'Spark'}
    ],
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'ServiceRole': 'EMR_DefaultRole',
}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'pinkman_walter-white',
    default_args=default_args,
    description='Taking moses.csv, normalizing it, splitting it and persisting it. Then trains and tests walter-white.',
    schedule_interval='@daily',
)

start_pinkman = EmrCreateJobFlowOperator(
    task_id='start_pinkman',
    job_flow_overrides=PINKMAN_JOB_FLOW_OVERRIDES,
    aws_conn_id='aws_default',
    emr_conn_id='emr_default',
    region_name='eu-central-1',
    dag=dag,
)

check_pinkman_result = EmrJobFlowSensor(
    task_id='check_pinkman_result',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='start_pinkman', key='return_value') }}",
    aws_conn_id='aws_default',
    dag=dag,
)

run_walter_white = AWSBatchOperator(
    task_id='run_walter-white',
    job_name='walter-white',
    job_queue=os.getenv('COMPUTE_ENVIRONMENT_JOB_QUEUE'),
    job_definition=os.getenv('WALTER_WHITE_JOB_DEFINITION'),
    aws_conn_id='aws_default',
    region_name='eu-central-1',
    overrides={},
    parameters={},
    dag=dag,
)

start_pinkman >> check_pinkman_result >> run_walter_white
