import csv
import os
import requests
from log import Log
from zk import ZK, const
from datetime import datetime
import uuid
import time

class AllParam :

    ## CONSTANCE
    EMPLOYEE_ID_INDEX = 0
    USER_ID_INDEX = 1
    WORK_SHIFT_ID_INDEX = 2
    TIME_WORK_INDEX = 3
    CHECK_IN_INDEX = 4
    CHECK_OUT_INDEX = 5
    CHECK_COUNT_INDEX = 6

    MODULE_ID_INDEX = 0
    MODULE_PING_INDEX = 1
    MODULE_STATUS_INDEX = 2
    MODULE_NAME_INDEX = 3
    MODULE_CONTROLLED_INDEX = 4
    MODULE_DEBUGER_INDEX = 5
    MODULE_SET_UP_STATUS_INDEX = 6
    MODULE_COMMU_STATUS_INDEX = 7
    MODULE_DESTINATION_INDEX = 8

    ## FILE CONFIG
    DATA_PATH   = './data'
    DATA_FILE   = DATA_PATH + '/user_datas.csv'
    CONFIG_PATH = './config'
    CONFIG_FILE = CONFIG_PATH + '/config.csv'

    ## RASPBERRY PI CONFIG
    DEBUG         = True
    MODULE_ID     = uuid.uuid4()
    MODULE_PING   = time.time()
    MODULE_NAME   = 'Raspberry Pi'
    MODULE_STATUS = 1
    MODULE_CONTROLLED = 'ZKTeco K60'
    MODULE_COMMU_STATUS = 1
    MODULE_DEBUGER = DEBUG
    MODULE_SET_UP_STATUS = True
    MODUEL_FIRMWARE_VERSION = "BETA"

    ## K60 CONNECTION CONFIG
    IP_ADDRESS  = '192.168.2.38'
    RUNNER = None

    ## FILE EXECHANGER
    DATA_WRITER = None
    DATA_READER = None
    CONFIG_WRITER = None
    CONFIG_READER = None
    DATA_CONTROLLER = None
    CONFIG_CONTROLLER = None

    API_UPDATE_URL = 'https://sys.apisupergourmet.com/api/employee/v1/employee/update-workday'

log = Log(True)
const_param = AllParam()

def main() :
    initailize()
    instance = set_up()
    if instance is not None :
        test_connected(instance)
        runtime(instance)
    else :
        log.error('MAIN', 'instance is none')

def set_up() :
    FUNC_NAME = 'SETUP'
    log.info(FUNC_NAME , 'Start setup')
    log.info(FUNC_NAME , 'Set datas into instance')
    file = open(const_param.CONFIG_FILE , mode='a+')
    file.seek(0)
    csv_reader = csv.reader(file)
    set_config(csv_reader)
    module_health_check()
    return ZK(const_param.IP_ADDRESS, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

def initailize() :
    FUNC_NAME = 'INITAIL'
    log.info(FUNC_NAME , 'Start initailize')
    main_dir = os.listdir('./')
    for file in main_dir :
        if file == 'config' :
            set_reader_writer()
            return log.info(FUNC_NAME , "Found file config")
    init_config_file()
    init_data_file()

def set_reader_writer() :
    FUNC_NAME = "SET"
    log.info(FUNC_NAME , "Set writer and reader")
    const_param.DATA_CONTROLLER = open(const_param.DATA_FILE, mode='a+')
    const_param.CONFIG_CONTROLLER = open(const_param.CONFIG_FILE, mode='a+')

def init_config_file() :

    FUNC_NAME = 'CONFIG FILE INIT'
    log.info(FUNC_NAME , 'Config file initing...')
    CONFIG_DATAS = [
        ["module_id", const_param.MODULE_ID],
        ["module_ping", const_param.MODULE_PING],
        ["module_status", const_param.MODULE_STATUS],
        ["module_name", const_param.MODULE_NAME],
        ["module_controlled" , const_param.MODULE_CONTROLLED],
        ["module_debuger", const_param.MODULE_DEBUGER],
        ["module_set_up_status" , const_param.MODULE_SET_UP_STATUS],
        ["module_commu_status" , const_param.MODULE_COMMU_STATUS],
        ["module_destination", const_param.IP_ADDRESS],
        ["module_firmware_version", const_param.MODUEL_FIRMWARE_VERSION]
    ]
    
    os.mkdir(const_param.CONFIG_PATH)
    file = open(const_param.CONFIG_FILE , mode='w' , newline='')
    csv.writer(file).writerows(CONFIG_DATAS)
    log.info(FUNC_NAME, "Finish setup config file")

def init_data_file() :

    FUNC_NAME = 'DATA FILE INIT'
    log.info(FUNC_NAME , 'Data file initing...')
    DATAS_HEADERS = [
        ["employee_id", "user_id" , "work_shift_id" , "time_work" , "check_in" , "check_out" , "check_count"],
    ]

    os.mkdir(const_param.DATA_PATH)
    const_param.DATA_CONTROLLER = open(const_param.DATA_FILE, mode='a+')
    file = open(const_param.DATA_FILE , mode='w' , newline='')
    csv.writer(file).writerows(DATAS_HEADERS)
    log.info(FUNC_NAME, "Finish setup data file")


def add_user_data(EMPLOYEE_ID , USER_ID , WORK_SHIFT , TIME_WORK , CHECK_IN , CHECK_OUT , CHECK_COUNT) :
    all_data_in_storage = list(csv.reader(const_param.DATA_READER)).append([EMPLOYEE_ID , USER_ID , WORK_SHIFT , TIME_WORK , CHECK_IN , CHECK_OUT , CHECK_COUNT])
    csv.writer(const_param.DATA_WRITER).writerows(all_data_in_storage)

def update_user_data(USER_ID , KEY_INDEX , VALUE) :
    datas = list(csv.reader(const_param.DATA_READER))
    for data in datas :
        if data[const_param.USER_ID_INDEX] == USER_ID :
            data[KEY_INDEX] = VALUE
    csv.writer(const_param.DATA_FILE).writerows(datas)

def user_check_count(USER_ID) :
    datas = list(csv.reader(const_param.DATA_READER))
    for data in datas :
        if data[const_param.USER_ID_INDEX] == USER_ID :
            return data[const_param.CHECK_COUNT_INDEX] % 2 != 0

def user_check_found(USER_ID) :
    found = False
    datas = list(csv.reader(const_param.DATA_READER))
    for data in datas :
        if data[const_param.USER_ID_INDEX] == USER_ID :
            found = True
    return found



def set_config(datas) :
    for index , data in enumerate(datas) :
        if index == const_param.MODULE_ID_INDEX :
            const_param.MODULE_ID = data[1]
        elif index == const_param.MODULE_PING_INDEX :
            const_param.MODULE_PING = data[1]
        elif index == const_param.MODULE_STATUS_INDEX :
            const_param.MODULE_STATUS = data[1]
        elif index == const_param.MODULE_NAME_INDEX :
            const_param.MODULE_NAME = data[1]
        elif index == const_param.MODULE_CONTROLLED_INDEX :
            const_param.MODULE_CONTROLLED = data[1]
        elif index == const_param.MODULE_DEBUGER_INDEX :
            const_param.MODULE_DEBUGER = bool(data[1])
        elif index == const_param.MODULE_SET_UP_STATUS_INDEX :
            const_param.MODULE_SET_UP_STATUS = bool(data[1])
        elif index == const_param.MODULE_COMMU_STATUS_INDEX :
            const_param.MODULE_COMMU_STATUS = data[1]
        elif index == const_param.MODULE_DESTINATION_INDEX :
            const_param.IP_ADDRESS = data[1]
        elif index == const_param.MODUEL_FIRMWARE_VERSION :
            const_param.MODUEL_FIRMWARE_VERSION = data[1]

def module_health_check() :
    FUNC_NAME = 'HEALTH'
    TIME = datetime.fromtimestamp(float(const_param.MODULE_PING)).strftime("%Y-%m-%d %H:%M:%S")
    log.info(FUNC_NAME , 'Module ID        :            ' + str(const_param.MODULE_ID))
    log.info(FUNC_NAME , 'Module Last Ping :            ' + TIME)
    log.info(FUNC_NAME , 'Module Status    :            ' + str(const_param.MODULE_STATUS))
    log.info(FUNC_NAME , 'Module Name      :            ' + str(const_param.MODULE_NAME))
    log.info(FUNC_NAME , 'Module Controlled  :          ' + str(const_param.MODULE_CONTROLLED))
    log.info(FUNC_NAME , 'Module Debuger Status :       ' + str(const_param.MODULE_DEBUGER))
    log.info(FUNC_NAME , 'Module Set Up Status  :       ' + str(const_param.MODULE_SET_UP_STATUS))
    log.info(FUNC_NAME , 'Module Communication Status : ' + str(const_param.MODULE_COMMU_STATUS))
    log.info(FUNC_NAME,  'Module Destination  :         ' + str(const_param.IP_ADDRESS))

        
    # file
    # connection = ZK(ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

## need to implemented
# def create_file():
#     FUNC_NAME = 'CREATE FILE'
#     log('[INFO][CREATE FILE] : Start Create file')
#     return

## need to implemented
def update_data():
    return

def test_connected(instance) :
    FUNC_NAME = "TEST"
    try:
        connector = instance.connect()
        connector.disable_device()
        connector.test_voice(24)
        connector.enable_device()
        log.info(FUNC_NAME , "Module found and runing ...")
    except Exception as e:
        log.error(FUNC_NAME , "{}".format(e))
            # print ("Process terminate : {}".format(e))
    finally:
        if connector :
            connector.disconnect()
        else :
            log.error(FUNC_NAME , "Connector not found")
    return

def runtime(instance) : 
    FUNC_NAME = "EVENT"
    log.info(FUNC_NAME , "Start running ..... ")
    while True :
        try:
            connector = instance.connect()
            connector.disable_device()
            for ATTENDANCE in connector.live_capture():
                if ATTENDANCE is None:
                    pass
                else:
                    USER_ID = str(ATTENDANCE.user_id)
                    if user_check_found(USER_ID) :
                        if user_check_count(ATTENDANCE.user_id) :
                            log.info(FUNC_NAME, "User ID " + str(ATTENDANCE.user_id) + " Check in")
                            update_user_data(ATTENDANCE.user_id, const_param.CHECK_OUT_INDEX , time.time())
                        else :
                            log.info(FUNC_NAME , "User ID " + str(ATTENDANCE.user_id) + " Check out")
                            update_user_data(ATTENDANCE.user_id, const_param.CHECK_IN_INDEX , time.time())
                    else :
                        log.error(FUNC_NAME , "User ID " + USER_ID +  " not found in list")

            connector.enable_device()
        except Exception as e:
            log.error(FUNC_NAME , "{}".format(e))
            # print ("Process terminate : {}".format(e))
        finally:
            if connector :
                connector.disconnect()
            else :
                log.error(FUNC_NAME , "Connector not found")