import time
import queue


def task_handler(task_list: queue.Queue(-1), sleep_second: int):
    while True:
        task = task_list.get()
        if task.task_type == "stop":
            break
        task.do()
