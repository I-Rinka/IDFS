import threading
from time import sleep
from typing import Text
from IDFS_EMU.emulator import drop_cluster
import IDFS_EMU.members as imu
import random
import IDFS_EMU.util as ut
import IDFS_EMU.config as conf
from client import config

total_request = 0
hit_count = 0
hit_old_count = 0

data_usage_lock = threading.Lock()
p2p_data_usage = 0
cloud_data_usage = 0


class newest_file(object):
    """docstring for newest_file."""

    def __init__(self):
        super(newest_file, self).__init__()
        self.newest_file_lock = threading.Lock()
        self.newest_file = {}
        self.file_count = {}

    def update_file(self, Afile: imu.file):
        self.newest_file_lock.acquire()
        self.newest_file[Afile.name] = Afile
        self.newest_file_lock.release()

    def get_all_new_file(self):
        rt = []
        self.newest_file_lock.acquire()
        for file_name in newest_file_table.newest_file:
            rt.append(newest_file_table.get_newest_file(file_name))
        self.newest_file_lock.release()
        return rt

    def get_file_count(file_name: str, device_cluster) -> int:
        count = 0
        dc = device_cluster.get_device_snapshot(True)
        for device in dc:
            for file in device.file_pool:
                if file.name == file_name:
                    count += 1
        return count

    def get_random_file(self):
        f = random.randint(0, len(self.newest_file)-1)
        i = 0
        for file in self.newest_file:
            if i == f:
                return self.newest_file[file]
            i = i+1

    def get_newest_hash(self, name: str):
        while not name in self.newest_file:
            pass
        return self.newest_file[name].hash

    def get_newest_file(self, name: str) -> imu.file:
        return self.newest_file[name]


newest_file_table = newest_file()


class device_cluster():
    """docstring for device_cluster."""

    def __init__(self):
        super(device_cluster, self).__init__()
        self.is_online = True
        self.active_cluster = []
        self.lonely_clients = []
        self.all_device = []
        self.cluster_lock = threading.Lock()

    def offline(self):
        self.is_online = False

    def online(self):
        self.is_online = True

    def add_active_device(self, device: imu.device):
        self.__add_device__(device, self.active_cluster)

    def add_lonely_device(self, device: imu.device):
        self.__add_device__(device, self.lonely_clients)

    def __add_device__(self, device: imu.device, cluster: list):
        self.cluster_lock.acquire()
        cluster.append(device)
        self.cluster_lock.release()
        self.all_device.append(device)

    def get_file(self, file_name: str):
        cfile = None
        for dvc in self.active_cluster:
            if cfile == None:
                cfile = dvc.get_file(file_name)
            else:
                tfile = dvc.get_file(file_name)
                if tfile is not None:
                    if tfile.timestamp > cfile.timestamp:
                        cfile = tfile
        if cfile is not None:  # data useage count
            data_usage_lock.acquire()
            global p2p_data_usage
            p2p_data_usage += cfile.size
            data_usage_lock.release()
            return cfile

        if self.is_online:
            for dvc in self.lonely_clients:
                if cfile == None:
                    cfile = dvc.get_file(file_name)
                    print("remote access")
                else:
                    tfile = dvc.get_file(file_name)
                    if tfile is not None:
                        if tfile.timestamp > cfile.timestamp:
                            cfile = tfile
                            print("remote access")
        if cfile is not None:  # data useage count
            data_usage_lock.acquire()
            global cloud_data_usage
            print("file_size"+str(cfile.size))
            cloud_data_usage += cfile.size
            data_usage_lock.release()

        return cfile

    def get_random_device(self, is_from_active: bool) -> imu.device:
        i = random.randint(0, 99)
        base = 0
        total_usage = 0

        if is_from_active:
            cluster = self.active_cluster
        else:
            cluster = self.lonely_clients

        self.cluster_lock.acquire()
        for dvc in cluster:
            total_usage += dvc.use_frequency
        for dvc in cluster:
            if base <= i and base+100*(dvc.use_frequency)/total_usage >= i:
                self.cluster_lock.release()
                return dvc
            else:
                base += 100*(dvc.use_frequency)/total_usage
        self.cluster_lock.release()
        return None

    def drop_device(self):
        if len(self.active_cluster) > 1:
            i = random.randint(0, 99)
            self.cluster_lock.acquire()
            total_usage = 0
            for dvc in self.active_cluster:
                total_usage += 1-dvc.use_frequency

            base = 0
            for dvc in self.active_cluster:
                if base <= i and base+100*(1-dvc.use_frequency)/total_usage >= i:
                    # drop cluster
                    self.active_cluster.remove(dvc)
                    self.lonely_clients.append(dvc)
                    break
                else:
                    base += 100*(1-dvc.use_frequency)/total_usage

            self.cluster_lock.release()

    def join_device(self):
        i = random.randint(0, 99)
        self.cluster_lock.acquire()
        total_usage = 0
        for dvc in self.lonely_clients:
            total_usage += 1-dvc.use_frequency

        base = 0
        for dvc in self.lonely_clients:
            if base <= i and base+100*(dvc.use_frequency)/total_usage >= i:
                # drop cluster
                self.lonely_clients.remove(dvc)
                self.active_cluster.append(dvc)
                break
            else:
                base += 100*(dvc.use_frequency)/total_usage

        self.cluster_lock.release()

    def get_device_snapshot(self, is_active: bool):
        rt = []
        self.cluster_lock.acquire()
        if is_active:
            for dvc in self.active_cluster:
                rt.append(dvc)
        else:
            for dvc in self.lonely_clients:
                rt.append(dvc)
        self.cluster_lock.release()
        return rt

    def get_all_device(self):
        return self.all_device


def user_get_file(IDFS_cluster: device_cluster):
    afile = newest_file_table.get_random_file()
    gfile = IDFS_cluster.get_file(afile.name)
    # data usage is inside IDFS_cluster.get_file
    global total_request
    total_request = total_request+1

    if gfile is None:
        print("miss hit")
    else:
        global hit_count
        hit_count = hit_count+1

        # current device download file
        if gfile.hash == newest_file_table.get_newest_hash(gfile.name):
            IDFS_cluster.get_random_device(True).add_file(gfile)
        else:
            global hit_old_count
            hit_old_count = hit_old_count+1

    print("total count:{tt}\nsuccess count:{st}\nold count:{ot}\nsuccess rate:{sr}"
          .format(tt=total_request, st=hit_count, ot=hit_old_count, sr=str(float(hit_count)/float(total_request)*100)+'%'))


def user_upload_file(Afile: imu.file, IDFS_cluster: device_cluster):
    d1 = IDFS_cluster.get_random_device(True)
    # strategy: copy once
    # while True:
    d2 = IDFS_cluster.get_random_device(True)
    #     if d1==d2 or len(IDFS_cluster.get_device_snapshot(True)) <= 1:
    #         break

    d1.add_file(Afile)
    if d2 != d1:
        d2.add_file(Afile)
        data_usage_lock.acquire()
        global p2p_data_usage
        p2p_data_usage += Afile.size
        data_usage_lock.release()
    newest_file_table.update_file(Afile)


def user_modify_file(IDFS_cluster: device_cluster):
    dvc = IDFS_cluster.get_random_device(True)
    mfile = newest_file_table.get_random_file()
    mfile = imu.file(mfile.name, ut.get_rhash(
    ), ut.get_now_time(), random.randint(0, conf.file_max_size))

    newest_file_table.update_file(mfile)
    dvc.add_file(mfile)


def IDFS_upload_cloud(IDFS_cluster: device_cluster):
    pass
    # if IDFS_cluster.is_online:
    #     active = IDFS_cluster.get_device_snapshot(True)

    #     for device in active:
    #         for file in device.file_pool:
    #             if file.hash == newest_file_table.get_newest_hash(file.name):
    #                 ld = IDFS_cluster.get_random_device(False)

    #                 if ld != None and ld != device and ut.get_now_time()-file.timestamp >= conf.old_file_threashold and newest_file.get_file_count(file.name, IDFS_cluster) <= 1:
    #                     ld.add_file(file)
    #                     data_usage_lock.acquire()
    #                     # add cloud update usage
    #                     print("upload"+file.name+"size"+str(file.size))
    #                     global cloud_data_usage
    #                     cloud_data_usage += file.size
    #                     data_usage_lock.release()


def IDFS_cleaner(IDFS_cluster: device_cluster):
    active = IDFS_cluster.get_device_snapshot(True)
    for device in active:
        for file in device.file_pool:
            nfile = newest_file_table.get_newest_file(file.name)
            if file.hash != nfile.hash:
                if nfile.size >= conf.big_file_threashold:
                    device.rm_file(file)
                else:
                    # delete duplicated files
                    if newest_file.get_file_count(file.name, IDFS_cluster) > 2:
                        if ut.get_now_time()-file.timestamp >= conf.old_file_threashold:
                            device.rm_file(file)

                    else:
                        data_usage_lock.acquire()
                        nnfile = newest_file_table.get_newest_file(file.name)
                        device.add_file(
                            nnfile)
                        global p2p_data_usage
                        p2p_data_usage += nnfile.size
                        data_usage_lock.release()


def get_stastictics(IDFS_cluster: device_cluster):
    fsize = 0
    fl = newest_file_table.get_all_new_file()
    for file in fl:
        fsize += file.size

    allsize = 0
    all_device = IDFS_cluster.all_device
    for device in all_device:
        for file in device.file_pool:
            allsize += file.size

    print("""
----------------
>
upload data:{ud}
p2p data:{pd}
file size:{fs}
all file size:{afs}
file ratio:{fr}
----------------
    """.format(ud=cloud_data_usage, pd=p2p_data_usage, fs=fsize, afs=allsize, fr=float(fsize)/float(allsize)))
