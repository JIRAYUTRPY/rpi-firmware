from zk import ZK, const

conn = None
# create ZK instance
zk = ZK('192.168.88.148', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    # users = conn.get_users()
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
    # datas = conn.get_attendance()
    # # print(data)
    # for data in datas:
    # live capture! (timeout at 10s)
    for attendance in conn.live_capture():
        if attendance is None:
        # implement here timeout logic
            pass
        else:
            print (attendance.timestamp, attendance.user_id) # Attendance object

    #if you need to break gracefully just set
    #   conn.end_live_capture = True
    #
    # On interactive mode,
    # use Ctrl+C to break gracefully
    # this way it restores timeout
    # and disables live capture
    #     print(data.uid)

    # Test Voice: Say Thank You
    conn.test_voice(10)
    device_name = conn.get_device_name()
    # print(device_name)
    # re-enable device after all commands already executed
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()