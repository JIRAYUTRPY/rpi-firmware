from typing import Union

from fastapi import FastAPI, HTTPException

from data_managements import get_times, get_users
from pydantic import BaseModel
import json

class CreateUser(BaseModel):
    name: str
    user_id: str
    group_id : str
    password: str

class Initialize(BaseModel):
    ip : str

class InitialEmployeeCode(BaseModel):
    employee_code : str
    work_shift_id : str


app = FastAPI(title="Raspberry PI Attendance time server.")

# @app.get("/users")
# def read_users(ip : str):
#     try :
#         data = get_users(ip)
#         status_code = 200
#         message = "Successfully"
#     except Exception as e:
#         data = []
#         status_code = 500
#         message = "{}".format(e)
#     return { "message" : message , "status_code" : status_code , "data" : data }

# @app.get("/user/{user_id}")
# def read_user(user_id : str , ip : str):
#     return { "message" : "Get user by user id" }

@app.post("/initialize")
async def initialize(infomation : Initialize , datas : list[InitialEmployeeCode]):

    users = get_users(ip_address=infomation.ip)

    if len(users) != len(datas) :
        raise HTTPException(status_code=404, detail="ข้อมูลในระบบไม่ตรงกับข้อมูลในอุปกรณ์")
    
    len_data = len(users)
    checker = 0
    for user in users :
        for data in datas :
            if user.user_id == data.employee_code :
                checker += 1
    
    if len_data != checker :
        raise HTTPException(status_code=404, detail="ข้อมูลในระบบไม่ตรงกับข้อมูลในอุปกรณ์")
    

    

    return { "detail" : "สำเร็จ" }

@app.get("/start")
def initialize(ip : Union[str, None] = None):
    return { "message" : "Create user" }

# @app.get("/times")
# def read_times(ip : str):
#     try :
#         data = get_times(ip)
#         status_code = 200
#         message = "Successfully"
#     except Exception as e:
#         data = []
#         status_code = 500
#         message = "{}".format(e)
#     return { "message" : message , "status_code" : status_code , "data" : data }

# @app.post("/initailize")
# def create_users(ip : str , data: CreateUser):
#     try :
#         res = create_users(ip , data)
#         print(res)
#         status_code = 200
#         message = "Creates Successfully"
#     except Exception as e:
#         res = []
#         status_code = 500
#         message = "{}".format(e)
#     return { "message" : message , "status_code" : status_code }

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/test")
# def test():
#     return {"TEST":"TEST"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}