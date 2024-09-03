from zk import ZK, const
from datetime import datetime

def get_users(ip_address):
    conn = None
    zk = ZK(ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.disable_device()
    users = conn.get_users()
    conn.enable_device()
    conn.disconnect()
    return users

def create_users(ip_address, data):
    conn = None
    zk = ZK(ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.disable_device()
    
    for info, index in data :
        conn.set_user(uid=index+1, name=info.name, privilege=const.USER_DEFAULT, password=info.password , group_id=info.group_id, user_id=info.user_id, card=0)
    conn.enable_device()
    conn.disconnect()

def get_times(ip_address):
    conn = None
    zk = ZK(ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = zk.connect()
    conn.disable_device()
    datas = conn.get_attendance()
    realdata = []
    now = datetime(2024, 9, 1)
    for data in datas :
        # datetime_object = datetime.strptime(data.timestamp,"%Y-%m-%dT%H:%M:%S")
        if data.timestamp >= now :
            print(data.timestamp.strftime("%B"))
            realdata.append(data)
    conn.enable_device()
    conn.disconnect()
    return realdata

        # for user in users:
        #     privilege = 'User'
        #     if user.privilege == const.USER_ADMIN:
        #         privilege = 'Admin'
        #     print ('+ UID #{}'.format(user.uid))
        #     print ('  Name       : {}'.format(user.name))
        #     print ('  Privilege  : {}'.format(privilege))
        #     print ('  Password   : {}'.format(user.password))
        #     print ('  Group ID   : {}'.format(user.group_id))
        #     print ('  User  ID   : {}'.format(user.user_id))
        # conn.test_voice(4)
        # device_name = conn.get_device_name()
        # print(device_name)
        # re-enable device after all commands already executed
            