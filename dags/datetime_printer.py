import time
from datetime import datetime

from airflow.decorators import (
    dag,
    task,
)


@dag(
    schedule_interval="1-59/2 * * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["example"],
)
def datetime_printer():
    @task()
    def datetime_printer():
        """
        Print the date and time for five minute.
        """

        for i in range(300):
            print(datetime.now().strftime(f"{i=} %FT%T"))
            time.sleep(1)

    datetime_printer()


datetime_printer = datetime_printer()
