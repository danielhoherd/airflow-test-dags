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
        "retries": 5,
    },
    tags=["should-fail"],
)
def datetime_printer_failing():
    @task()
    def datetime_printer_failing():
        """
        Print the date and time for a while then raise an exception.
        """

        for i in range(30):
            print(datetime.now().strftime(f"{i=} %FT%T"))
            time.sleep(1)

        raise Exception("This is a forced exception to test exception handling.")

    datetime_printer_failing()


datetime_printer_failing = datetime_printer_failing()
