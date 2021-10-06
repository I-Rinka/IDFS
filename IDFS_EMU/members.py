import time
import threading


class file(object):
    """IDFS file."""

    def __init__(self, name, hash, timestamp, size):
        super(file, self).__init__()
        self.name = name
        self.hash = hash
        self.timestamp = timestamp
        self.size = size


class device(object):
    """IDFS device."""

    def __init__(self, device_id, use_frequnecy):
        super(device, self).__init__()
        self.device_id = device_id
        self.use_frequency = use_frequnecy
        self.fp_lock = threading.Lock()
        self.file_pool = []

    def add_file(self, afile: file):
        self.fp_lock.acquire()
        gfile = self.get_file(afile.name)
        if gfile is not None:
            self.file_pool.remove(gfile)
        self.file_pool.insert(0, afile)
        self.fp_lock.release()

    def get_file(self, file_name: str):
        for afile in self.file_pool:
            if file_name == afile.name:
                return afile
        return None

    def rm_file(self, afile: file):
        self.fp_lock.acquire()
        if afile in self.file_pool:
            self.file_pool.remove(afile)
        self.fp_lock.release()
