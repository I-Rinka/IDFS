class Device(metaclass=abc.ABCMeta):

    def GetDeviceName(self):
        '子类必须定义读功能'
        pass

    def GetDeviceStatus(self):
        '子类必须定义写功能'
        pass

    def AssignDeviceStatus(self):
        '子类必须定义写功能'
        pass