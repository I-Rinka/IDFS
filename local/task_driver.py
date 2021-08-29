import time
import queue

TASK_QUEUE = queue.Queue(maxsize=-1)

def task_handler(sleep_second: int):
    while True:
        task = TASK_QUEUE.get()
        if task.task_type == "stop":
            break
        task.do()
