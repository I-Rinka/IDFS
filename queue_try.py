from threading import Thread
from queue import Queue

import random
import time

task_list = Queue(-1)


def func1():
    while True:
        slpt = random.randint(0, 3)
        print(slpt)
        time.sleep(slpt)
        task_list.put("哈哈哈，时间是:%s" % slpt)


def func2():
    i = 0
    while True:
        print(i)
        print(task_list.get()) #这个东西果然会自己阻塞
        i = i+1


# 创建 Thread 实例
t1 = Thread(target=func1, args=())
t2 = Thread(target=func2, args=())

# 启动线程运行
t1.start()
t2.start()

# 等待所有线程执行完毕
t1.join()  # join() 等待线程终止，要不然一直挂起
t2.join()
