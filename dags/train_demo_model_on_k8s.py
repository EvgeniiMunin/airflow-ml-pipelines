from airflow import models
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.models.variable import Variable
from airflow.utils.dates import days_ago
from kubernetes.client import V1EnvVar

with models.DAG(
    "example_train_model",
    schedule_interval=None,  # Override to match your needs
    start_date=days_ago(1),
    tags=["tags"],
) as dag:
    secret_aws_key_id = Secret(
        # Expose the secret as environment variable.
        deploy_type="env",
        # The name of the environment variable, since deploy_type is `env` rather
        # than `volume`.
        deploy_target="AWS_ACCESS_KEY_ID",
        # Name of the Kubernetes Secret
        secret="aws-s3-secret",
        # Key of a secret stored in this Secret object
        key="AWS_ACCESS_KEY_ID",
    )

    secret_aws_access_key = Secret(
        # Expose the secret as environment variable.
        deploy_type="env",
        # The name of the environment variable, since deploy_type is `env` rather
        # than `volume`.
        deploy_target="AWS_SECRET_ACCESS_KEY",
        # Name of the Kubernetes Secret
        secret="aws-s3-secret",
        # Key of a secret stored in this Secret object
        key="AWS_SECRET_ACCESS_KEY",
    )


    train_model = KubernetesPodOperator(
        task_id="train-heart-ml-model",
        name="train-heart-ml-model",
        cmds=["python", "train.py"],
        arguments=[
            "-d",
            "datasets/heart.csv",
            "-o",
            "models/heart_model_1.pkl",
            "--s3-bucket",
            "{{ var.value.bucket_name }}",
        ],
        secrets=[secret_aws_key_id, secret_aws_access_key],
        namespace=Variable.get("namespace"),
        service_account_name="airflow-scheduler",
        image="mikhailmar/training-job:pr-3",
    )
