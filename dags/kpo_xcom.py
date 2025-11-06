import logging

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

log = logging.getLogger(__name__)

with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
    namespace = f.read()

# https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-does-xcom-work
with DAG(
    dag_id="example_xcom_task",
    default_args={"owner": "airflow"},
    start_date=days_ago(2),
    schedule_interval=None,
    tags=["core"],
) as dag:
    write_xcom = KubernetesPodOperator(
        namespace=namespace,
        cmds=["sh", "-c", "mkdir -p /airflow/xcom/ ; echo '[1,2,3,4]' > /airflow/xcom/return.json ;"],
        name="write-xcom",
        image="quay.io/astronomer/ap-init:3.21.3-5",
        do_xcom_push=True,
        on_finish_action="delete_pod",
        in_cluster=True,
        task_id="write-xcom",
        get_logs=True,
    )

    pod_task_xcom_result = BashOperator(
        bash_command="echo \"{{ task_instance.xcom_pull('write-xcom')[0] }}\"",
        task_id="pod_task_xcom_result",
    )

    write_xcom >> pod_task_xcom_result
