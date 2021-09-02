import time
import queue
import local.task as tsk


def task_handler(sleep_second: int):
    while True:
        task = tsk.TASK_QUEUE.get()
        if task.task_type == "stop":
            break
        task.do()
