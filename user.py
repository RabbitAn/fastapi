from models import User
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from jwt_permiss import create_jwt,verify_jwt,get_current_user
from models import User  # 你的 ORM 模型


class UserDto(BaseModel):
    username: str = None
    email: str = None
    password: str = None


user_controller=APIRouter()

@user_controller.get("/users",summary="获取所有用户")
async def get_users():
    users = await User.all()
    user={"user":"xiaoming","password":"123456"}
    token = create_jwt(user)
    return token

#通过条件筛查
@user_controller.post("/users/search",summary="通过条件筛查用户")
async def search_users(user:UserDto,current_user=Depends(get_current_user)):
    query = {}
    if user.username:
        query["username__icontains"] =user. username
    if user.email:
        query["email__icontains"] =user. email
    users = await User.filter(**query)
    return users

#插入用户
@user_controller.post("/users",summary="插入用户")
async def create_user(username: str, email: str, password: str):
    user = await User.create(username=username, email=email, password=password)
    return user

#更新用户
@user_controller.put("/users/{user_id}",summary="更新用户")
async def update_user(user_id: int, username: str = None, email: str = None, password: str = None):
    user = await User.get(id=user_id)
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = password
    await user.save()
    return user

#删除用户
@user_controller.delete("/users/{user_id}",summary="删除用户")
async def delete_user(user_id: int):
    user = await User.get(id=user_id)
    await user.delete()
    return {"message": "User deleted successfully"}

