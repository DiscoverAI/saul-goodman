from datetime import timedelta

from airflow import DAG
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.sensors.emr_job_flow_sensor import EmrJobFlowSensor
from airflow.utils.dates import days_ago

SPARK_STEPS = [
    {
        'Name': 'pinkman',
        'ActionOnFailure': 'TERMINATE_CLUSTER',
        'HadoopJarStep': {
            'Jar': 's3://sars-cov-2-25309b4013524/pinkman/pinkman-job.jar'
        }
    }
]

JOB_FLOW_OVERRIDES = {
    'Name': 'Pinkman',
    'ReleaseLabel': 'emr-6.0.0',
    "LogUri": "s3://sars-cov-2-25309b4013524/pinkman/emr-logs",
    'Instances': {
        "Ec2KeyName": "tuco-key",
        'InstanceGroups': [
            {
                'Name': 'Master nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1,
            },
            {
                'Name': 'Core nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 3,
            }
        ],
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False,
    },
    'Steps': SPARK_STEPS,
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'ServiceRole': 'EMR_DefaultRole',
}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
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

job_flow_creator = EmrCreateJobFlowOperator(
    task_id='create_job_flow',
    job_flow_overrides=JOB_FLOW_OVERRIDES,
    aws_conn_id='aws_default',
    emr_conn_id='emr_default',
    region_name='eu-central-1',
    dag=dag,
)

job_sensor = EmrJobFlowSensor(
    task_id='check_job_flow',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_job_flow', key='return_value') }}",
    aws_conn_id='aws_default',
    dag=dag,
)

job_flow_creator >> job_sensor
