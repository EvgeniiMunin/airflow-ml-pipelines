# airflow-ml-pipelines

main -- даги для среды prod
stage -- даги для среда stage


Неавтоматизированные шаги для поднятия airflow 
~~~
kubectl create namespace airflow-prod
kubectl create namespace airflow-stage

~~~

~~~
kubectl create secret -n airflow-stage generic aws-s3-secret --from-literal=AWS_ACCESS_KEY_ID=NONO --from-literal=AWS_SECRET_ACCESS_KEY=NONO
~~~

~~~
kubectl create secret -n airflow-prod generic aws-s3-secret \                  
  --from-literal=AWS_ACCESS_KEY_ID=NONO \
  --from-literal=AWS_SECRET_ACCESS_KEY=NONO
~~~

~~~
helm install -n airflow-prod airflow apache-airflow/airflow 
    --set dags.gitSync.enabled=True 
    --set dags.gitSync.repo=https://github.com/demo-ml-cicd/airflow-ml-pipelines.git
    --set dags.gitSync.branch=main 
    --set dags.gitSync.subPath="dags/" 
~~~

~~~
helm install -n airflow-stage airflow apache-airflow/airflow \
    --set dags.gitSync.enabled=True 
    --set dags.gitSync.repo=https://github.com/demo-ml-cicd/airflow-ml-pipelines.git
    --set dags.gitSync.branch=stage 
    --set dags.gitSync.subPath="dags/" 
~~~

~~~
kubectl apply -f rbac/airflow-rbac-stage.yaml
kubectl apply -f rbac/airflow-rbac-prod.yaml
~~~
