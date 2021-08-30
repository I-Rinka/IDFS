# Maintain a device database for local use. Make decision to send data to which device
import local.device as dvc
import queue
import util.tools as ut
import threading
import time


phone_weight = 100
server_weight = 200
laptop_weight = 50


def get_weight(dev_row):
    dev = dev_row["device"]
    if dev.device_type == dvc.device_phone:
        return phone_weight
    elif dev.device_type == dvc.device_server:
        return server_weight
    elif dev.device_type == dvc.device_laptop:
        return laptop_weight
    return 1


def compare(x, y):
    if xGty(x, y):
        return 1
    else:
        return -1


def xGty(x, y):
    weight_x = get_weight(x)
    weight_y = get_weight(y)

    last_time_x = x["last_time"]
    last_time_y = y["last_time"]

    if weight_x+last_time_x > weight_y+last_time_y:
        return True
    return False


class DeviceList(object):
    """docstring for DeviceList."""

    def __init__(self):
        super(DeviceList, self).__init__()
        self.expire_time = 5
        self.dev_list = {}
        self.available = []

    def manage_thread(self):
        while True:
            time.sleep(self.expire_time)
            now_time = ut.GetIntTimeStamp()
            for dev in self.available:
                if now_time - dev["last_time"]:
                    self.available.remove(dev)

    def get_top1_dev(self):
        self.sort_avail_list()
        if len(self.available) == 0:
            return None
        return self.available[0]["device"]

    def find_device(self, device: dvc.Device):
        if not self.dev_list.__contains__(device.device_id):
            self.dev_list[device.device_id] = {
                "device": device, "task_queue": queue.Queue(), "last_time": -1}

    def update_device(self, device: dvc.Device):  # 只有被动连接发送心跳包等才更新信息
        if self.dev_list.__contains__(device.device_id):
            self.dev_list[device.device_id]["last_time"] = ut.GetIntTimeStamp()

        self.dev_list[device.device_id] = {
            "device": device, "task_queue": queue.Queue(), "last_time": ut.GetIntTimeStamp()}

        self.available.append(self.dev_list[device.device_id])

    def remove_avail_list(self, device: dvc.Device):
        self.available.remove(self.dev_list[device.device_id])

    def sort_avail_list(self):
        self.available.sort(cmp=compare)
