"""test dag to run a task using the KubernetesPodOperator. When we run tasks using RBAC we need to make sure that
Airflow can launch pods and monitor them.
"""
from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.utils.dates import days_ago
from kubernetes.client import models as k8s

NAMESPACE = conf.get("kubernetes", "NAMESPACE")
# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
in_cluster = True

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="k8_pod_operator",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["k8s"],
) as dag:
    task = KubernetesPodOperator(
        task_id="nsenter",
        namespace=NAMESPACE,
        in_cluster=True,
        kubernetes_conn_id="",
        is_delete_operator_pod=False,
        full_pod_spec=k8s.V1Pod(
            spec=k8s.V1PodSpec(
                host_pid=True,
                host_network=True,
                containers=[
                    k8s.V1Container(
                        name="nsenter",
                        image="alexeiled/nsenter:2.34",
                        command=["/nsenter", "--all", "--target=1", "--", "bash", "-c", "hostname -f && id && ps -ef"],
                        security_context=k8s.V1SecurityContext(privileged=True),
                    )
                ],
            )
        ),
        get_logs=True,
    )
