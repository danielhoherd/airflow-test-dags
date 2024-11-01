import sys
import time
from datetime import datetime

from airflow.decorators import (
    dag,
    task,
)


@dag(
    schedule_interval="*/5 * * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["example"],
)
def oom_creator():
    @task()
    def bytearray_grower():
        """
        Cause an OOM by using more and more memory through bytearrays.
        """

        this_list = []
        i = 0

        while i := i + 1:
            this_list.append(bytearray(1048519))  # make a bytearray that uses exactly 1048576 bytes
            total_bytes = sum(sys.getsizeof(x) for x in this_list)
            print(f"{i=} {total_bytes=} {hex(total_bytes)=} {bin(total_bytes)=}")
            time.sleep(0.05)

    bytearray_grower()


oom_creator = oom_creator()
