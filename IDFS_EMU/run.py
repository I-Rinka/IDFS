import threading
import IDFS_EMU.operation as iop
import IDFS_EMU.members as imu
import IDFS_EMU.util as ut
import IDFS_EMU.config as conf
import random

file_count=conf.file_count

def User_th():
    user_time = ut.get_now_time()
    user_gf_t = user_time
    user_che_t = user_time
    user_md_t = user_time
    user_up_t = user_time
    while True:
        # get file
        gf_t = random.randrange(conf.user_get_file_interval-conf.user_op_time_divia,
                                conf.user_get_file_interval+conf.user_op_time_divia)
        if ut.get_now_time()-user_gf_t >= gf_t:
            iop.user_get_file(cluster)
            user_gf_t = ut.get_now_time()
        

        # change environment
        che_t = random.randrange(conf.user_env_change_interval-conf.user_op_time_divia,
                                 conf.user_env_change_interval+conf.user_op_time_divia)
        if ut.get_now_time()-user_che_t >= che_t:
            if random.randint(0,1)==0:
                cluster.join_device()
            else:
                cluster.drop_device()

            if random.randint(0,99)>conf.device_offline_probility*100:
                cluster.online()
            else:
                print("offline")
                cluster.offline()

            user_che_t = ut.get_now_time()


        global file_count
        # upload file
        up_t = random.randrange(conf.user_upload_file_interval-conf.user_op_time_divia,
                                conf.user_upload_file_interval+conf.user_op_time_divia)
        if ut.get_now_time()-user_up_t >= up_t > 0 and file_count>0:
            file_count-=1
            user_up_t = ut.get_now_time()
            Afile=imu.file('/'+str(file_count),ut.get_rhash(),ut.get_now_time(),random.randint(0,conf.file_max_size))

            iop.user_upload_file(Afile,cluster)

        # modify file
        md_t = random.randrange(conf.user_modify_file_interval-conf.user_op_time_divia,
                                conf.user_modify_file_interval+conf.user_op_time_divia)
        if ut.get_now_time()-user_md_t >= md_t:
            
            iop.user_modify_file(cluster)
            user_md_t = ut.get_now_time()


def IDFS_th():
    while True:
        IDFS_cleaner_time=ut.get_now_time()
        IDFS_upload_time=ut.get_now_time()
        if ut.get_now_time()-IDFS_cleaner_time>=conf.IDFS_cleaner_interval:
            iop.IDFS_cleaner(cluster)

        if ut.get_now_time()-IDFS_upload_time>=conf.IDFS_upload_remote_interval:
            iop.IDFS_upload_cloud(cluster)
            iop.get_stastictics(cluster)
        
        # if ut.get_now_time()-IDFS_upload_time>=10000:

# initialize

cluster=iop.device_cluster()

cluster.add_active_device(imu.device("phone", 0.10))
cluster.add_active_device(imu.device("laptop", 0.10))
cluster.add_active_device(imu.device("tablet", 0.20))

cluster.add_lonely_device(imu.device("desktop", 0.01))

iop.user_upload_file(imu.file("/fst",ut.get_rhash(),ut.get_now_time(),random.randint(0,conf.file_max_size)),cluster)

if __name__ == "__main__":
    threading.Thread(target=User_th).start()
    threading.Thread(target=IDFS_th).start()