from airflow import models
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.utils.dates import days_ago

with models.DAG(
    "example_train_model",
    schedule_interval=None,  # Override to match your needs
    start_date=days_ago(1),
    tags=["example"],
) as dag:
    train_model = KubernetesPodOperator(
        task_id="train-heart-ml-model",
        name="train-heart-ml-model",
        cmds=[
            "-d",
            "datasets/heart.csv",
            "-o",
            "models/heart_model.pkl",
            "--s3_bucket",
            "demo-cicd-made",
        ],
        namespace="airflow-stage",
        service_account_name="airflow-scheduler",
        image="mikhailmar/training-job:pr-1",
    )
