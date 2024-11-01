import os
import time
from datetime import datetime

from airflow.decorators import (
    dag,
    task,
)


@dag(
    schedule_interval="*/2 * * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["example"],
)
def pid_killer():
    @task()
    def kill_pid(pid=7, signal=9, seconds=15):
        """
        Kill a pid with the given signal.
        """

        print(f"Killing {pid=} with {signal=} in {seconds=}")
        time.sleep(seconds)
        os.kill(pid, signal)

    kill_pid()


pid_killer = pid_killer()
