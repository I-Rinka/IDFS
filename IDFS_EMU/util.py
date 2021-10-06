import random
import time
def get_rhash():
    return random.randint(0,0x3f3f3f3f3f)

def get_now_time():
    return time.time_ns()
    