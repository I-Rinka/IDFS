import threading
import IDFS_EMU.members as imu
import random
import IDFS_EMU.util as ut

device_offline_probility = 0.2
file_max_size = 1000
big_file_threashold = 900
file_count = 100

user_env_change_interval = 1000
user_get_file_interval = 100
user_upload_file_interval = 200
user_modify_file_interval = 100
user_op_time_divia = 50

IDFS_update_interval = 1
IDFS_upload_remote_interval = IDFS_update_interval*100


request_time = 0
hit_time = 0
hit_old_time = 0

newest_file = {}
active_cluster = []
lonely_clients = []
offline_device = []
drop_groups = []  # clients are disconnect at the same time

newest_file_lock=threading.Lock()


def get_random_file():
    f = random.randint(0, len(newest_file)-1)
    i = 0
    for file in newest_file:
        if i == f:
            return newest_file[file]
        i = i+1


def drop_cluster():
    groups = []
    for dvc in active_cluster:
        if len(active_cluster) <= 1:
            break
        i = random.randint(0, 99)
        if dvc.use_frequency*100 < i:
            active_cluster.remove(dvc)
            groups.append(dvc)

    i = random.randint(0, 99)
    if device_offline_probility*100 > i:
        offline_device.extend(groups)
    else:
        lonely_clients.extend(groups)
    drop_groups.append(groups)


def join_cluster():
    if len(drop_groups)>1:
        i = random.randint(0, len(drop_groups)-1)
        active_cluster.extend(drop_groups[i])
        for dvc in drop_groups:
            if dvc in lonely_clients:
                lonely_clients.remove(dvc)
            if dvc in offline_device:
                offline_device.remove(dvc)


def get_file(file_name: str):
    cfile = None
    for dvc in active_cluster:
        if cfile == None:
            cfile = dvc.get_file(file_name)
        else:
            tfile = dvc.get_file(file_name)
            if tfile is not None:
                if tfile.timestamp > cfile.timestamp:
                    cfile = tfile
    if cfile is not None:
        return cfile

    for dvc in lonely_clients:
        if cfile == None:
            cfile = dvc.get_file(file_name)
            print("remote access")
        else:
            tfile = dvc.get_file(file_name)
            if tfile is not None:
                if tfile.timestamp > cfile.timestamp:
                    cfile = tfile
                    print("remote access")
    return cfile


def upload_file(afile: imu.file):
    for dvc in active_cluster:
        dvc.add_file(afile)


def upload_remote(afile: imu.file):
    if len(lonely_clients)>=1:
        t = random.randint(0, len(lonely_clients)-1)
        i = 0
        for dv in lonely_clients:
            if i == t:
                dv.add_file(afile)
                return
            i += 1


user_time = ut.get_now_time()

IDFS_time = ut.get_now_time()

rd = 0


def user_OP():
    user_gf_t = user_time
    user_che_t = user_time
    user_md_t = user_time
    user_up_t = user_time
    while True:
        global rd
        rd = rd+1
        # current using device
        all_freq = 0
        i = random.randint(0, 9)
        for dev in active_cluster:
            all_freq += dev.use_frequency
        calc = 0
        current_using_device = active_cluster[0]
        for dev in active_cluster:
            if calc <= i and calc+10*dev.use_frequency/all_freq >= i:
                current_using_device = dev
                break
            calc = calc+10*dev.use_frequency/all_freq

        # get file
        gf_t = random.randrange(user_get_file_interval-user_op_time_divia,
                                user_get_file_interval+user_op_time_divia)
        if ut.get_now_time()-user_gf_t >= gf_t:

            afile = get_random_file()
            gfile = get_file(afile.name)

            global request_time 
            request_time = request_time+1
            if gfile is None:
                print("miss hit")
            else:
                global hit_time
                hit_time = hit_time+1

                # current device download file
                if gfile.hash == newest_file[gfile.name].hash:
                    current_using_device.add_file(gfile)
                else:
                    global hit_old_time
                    hit_old_time = hit_old_time+1

                user_gf_t = ut.get_now_time()

            print("total count:{tt}\nsuccess count:{st}\nold count:{ot}\nsuccess rate:{sr}"
                  .format(tt=request_time, st=hit_time, ot=hit_old_time, sr=str(float(hit_time)/float(request_time)*100)+'%'))

        # change environment
        che_t = random.randrange(user_env_change_interval-user_op_time_divia,
                                 user_env_change_interval+user_op_time_divia)
        if ut.get_now_time()-user_che_t >= che_t:
            p = random.randint(0, 99)
            if p < user_env_change_interval*100:
                if random.randint(0, 99) >= 50:
                    drop_cluster()
                else:
                    join_cluster()
            user_che_t = ut.get_now_time()

        # upload file
        up_t = random.randrange(user_upload_file_interval-user_op_time_divia,
                                user_upload_file_interval+user_op_time_divia)

        global file_count
        if ut.get_now_time()-user_up_t >= up_t and file_count > 0:
            file_count = file_count-1
            ufile = imu.file('/'+str(rd), ut.get_rhash(),
                             ut.get_now_time(), random.randint(0, file_max_size))
            

            newest_file_lock.acquire()
            upload_file(ufile)
            newest_file[ufile.name] = ufile
            newest_file_lock.release()

            user_up_t = ut.get_now_time()

        # modify file
        md_t = random.randrange(user_modify_file_interval-user_op_time_divia,
                                user_modify_file_interval+user_op_time_divia)
        if ut.get_now_time()-user_md_t >= md_t:
            mfile = get_random_file()
            mfile = imu.file(mfile.name, ut.get_rhash(
            ), ut.get_now_time(), random.randint(0, file_max_size))

            newest_file[mfile.name] = mfile  # new file changes

            if get_file(mfile.name) is not None:
                current_using_device.add_file(mfile)
            user_md_t = ut.get_now_time()

def check_file_size():
    pass

def IDFS_OP():
    while True:
        if ut.get_now_time()-IDFS_time > IDFS_update_interval:
            active_files = {}
            for dev in active_cluster:
                for file in dev.file_pool:
                    can_add = True

                    if file not in active_files:
                        active_files[file.name] = 0

                    # upload_file(newest_file[file.name])

                    newest_file_lock.acquire()
                    if not newest_file[file.name].hash == file.hash:
                        if newest_file[file.name].size > big_file_threashold:
                            # remove big file
                            dev.rm_file(file)
                            can_add = False
                        else:
                            # update small file
                            dev.add_file(newest_file[file.name])

                    if ut.get_now_time() - file.timestamp > IDFS_upload_remote_interval and newest_file[file.name].hash == file.hash:
                        upload_remote(file)
                    newest_file_lock.release()

                    if can_add:
                        active_files[file.name] = active_files[file.name]+1

            newest_file_lock.acquire()
            # remove duplicate old file
            for dev in active_cluster:
                for file in dev.file_pool:
                    if file.name in active_files and active_files[file.name] >= 2 and newest_file[file.name].hash != file.hash:
                        print("delete one file")
                        dev.rm_file(file)
            newest_file_lock.release()


if __name__ == "__main__":
    IDFS_thread = threading.Thread(target=IDFS_OP,)
    user_thread = threading.Thread(target=user_OP,)

    active_cluster.append(imu.device("phone", 0.99))
    active_cluster.append(imu.device("laptop", 0.60))
    active_cluster.append(imu.device("tablet", 0.80))

    lonely_clients.append(imu.device("NAS", 0.05))
    lonely_clients.append(imu.device("desktop", 0.10))

    fst_file = imu.file("fst", ut.get_rhash(), ut.get_now_time(), 1)
    upload_file(fst_file)
    newest_file[fst_file.name] = fst_file

    IDFS_thread.start()
    user_thread.start()
