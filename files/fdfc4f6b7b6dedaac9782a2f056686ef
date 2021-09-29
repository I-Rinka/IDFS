import requests
import util as ut

def post_file():
    header = {"Authorization": "{}".format(
    ut.GetMyID()), "task_type": "{}".format("post_file")}
    r = requests.post("http://127.0.0.1:12345/haixing",
                    headers=header, data="haha", timeout=5)
    print(r.content)
    print(r.status_code)

def stop():
    header = {"Authorization": "{}".format(
    ut.GetMyID()), "task_type": "{}".format("stop")}
    r = requests.post("http://127.0.0.1:12345/haixing",
                    headers=header, data="haha", timeout=5)
    print(r.content)
    print(r.status_code)


def get_file():
    header = {"Authorization": "{}".format(
    ut.GetMyID()), "task_type": "{}".format("get_file")}
    r = requests.get("http://127.0.0.1:12345/haixing",
                    headers=header, timeout=5)
    print(r.content)
    print(r.status_code)

stop()