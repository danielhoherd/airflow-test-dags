from datetime import datetime, timedelta

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="failover_demo",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    extract_users = BashOperator(
        task_id="extract_users",
        bash_command="echo 'Extracting user data...' && sleep 30",
    )

    extract_orders = BashOperator(
        task_id="extract_orders",
        bash_command="echo 'Extracting order data...' && sleep 30",
    )

    transform_users = BashOperator(
        task_id="transform_users",
        bash_command="echo 'Transforming user data...' && sleep 30",
    )

    transform_orders = BashOperator(
        task_id="transform_orders",
        bash_command="echo 'Transforming order data...' && sleep 30",
    )

    join_datasets = BashOperator(
        task_id="join_datasets",
        bash_command="echo 'Joining datasets...' && sleep 30",
    )

    validate = BashOperator(
        task_id="validate",
        bash_command="echo 'Validating results...' && sleep 20",
    )

    load = BashOperator(
        task_id="load",
        bash_command="echo 'Loading to warehouse...' && sleep 20",
    )

    notify = BashOperator(
        task_id="notify",
        bash_command="echo 'Pipeline complete!'",
    )

    # Parallel extracts → parallel transforms → join → validate → load → notify
    extract_users >> transform_users >> join_datasets
    extract_orders >> transform_orders >> join_datasets
    join_datasets >> validate >> load >> notify
