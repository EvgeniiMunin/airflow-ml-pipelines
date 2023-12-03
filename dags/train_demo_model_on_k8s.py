from airflow import models
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.operators.bash import BashOperator
from airflow.models.variable import Variable
from airflow.utils.dates import days_ago
from kubernetes.client import V1EnvVar

"""
single stage DAG
"""

with models.DAG(
    "example_train_model",
    schedule_interval=None,  # Override to match your needs
    start_date=days_ago(1),
    tags=["example"],
) as dag:
    secret_volume = Secret(
        deploy_type='volume',
        # Path where we mount the secret as volume
        deploy_target='/var/secrets/google',
        # Name of Kubernetes Secret
        secret='service-account',
        # Key in the form of service account file name
        key='service-account.json'
    )

    train_model = KubernetesPodOperator(
        task_id="train-heart-ml-model",
        name="train-heart-ml-model",
        cmds=["python", "train.py"],
        arguments=[
            "-d",
            "datasets/data.csv", #"datasets/heart.csv",
            "-o",
            "models/model.csv", #"models/heart_model.pkl", #"models/heart_model_1.pkl",
            "--s3-bucket",
            "{{ var.value.bucket_name }}",
            "--endpoint-url",
            "https://s3.us-east-1.amazonaws.com",
        ],
        secrets=[secret_volume],
        env_vars=[
            V1EnvVar('GOOGLE_APPLICATION_CREDENTIALS', '/var/secrets/google/service-account.json')
        ],
        namespace="airflow-stage", #Variable.get("namespace"),
        service_account_name="airflow-scheduler",
        image="evgeniimunin/training-job:main",
    )
    
    t2 = BashOperator(
        task_id="sleep", bash_command="sleep 5",
    )
    
    train_model >> t2

