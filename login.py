from fastapi import APIRouter
from models import User
from jwt_permiss import create_jwt


login_controller=APIRouter()

@login_controller.post("/login",summary="用户登录")
async def user_login(username: str, password: str):
     res= await  User.get(username=username, password=password)
     if res:
        token=  create_jwt({"username":username,"password":password})
        return {"message": "登录成功","userName":f"username","token":f"{token}"}
     else:
         return {"message": "用户名或密码错误"}

