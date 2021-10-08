import IDFS_EMU.members as imu
import time
import random
client=imu.device(1,0.9)

for i in range(10):
    f=imu.file("/fst",i,timestamp=time.time(),size=100+i)
    client.add_file(f)

for i in range(3):
    f=imu.file("/scd"+str(i),random.randint(0,0x3f3f3f3f3f),timestamp=time.time(),size=100+i)
    client.add_file(f)
    print(f.__dict__)


# print(client.get_file("/fst").__dict__)
# print(client.get_file("/scd2").__dict__)
for file in client.file_pool:
    print(file.__dict__)