from datetime import datetime

from airflow.decorators import (
    dag,
    task,
)


def make_marker_line(length, fill_char="_"):
    """Generate a line of a given length with markers at every 10th position.

    The first character of the marker indicates the position of the value of the
    marker. Incomplete markers are truncated, so you will have to infer their
    value."""
    result = []
    i = 1
    while i <= length:
        if i % 10 == 0:
            marker = str(i)
            result.append(marker)
            i += len(marker)
        else:
            result.append(fill_char)
            i += 1
    return "".join(result)[:length]


@dag(
    schedule_interval="1-59/2 * * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["example"],
)
def long_line_printer():
    @task()
    def long_line_printer():
        """
        Print increasingly long lines
        """

    for i in range(0, 33000, 128):
        line = make_marker_line(i + 1)
        print(line)


long_line_printer = long_line_printer()
