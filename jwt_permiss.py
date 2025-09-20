import jwt
import datetime
from fastapi import Request, HTTPException

#定义密匙
SECRET_KEY = "your_secret_key"

#生成jwt
def create_jwt(data):
    try:
        pyload={
            "data": data,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # 过期时间
            "iat": datetime.datetime.utcnow()  # 签发时间
        }
        token = jwt.encode(pyload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        return f"生成 JWT 时出错: {str(e)}"


# 验证 JWT
def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token 已过期"
    except jwt.InvalidTokenError:
        return "无效的 Token"


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="缺少或无效的 Authorization 头")
    token = auth_header.split(" ")[1]
    return verify_jwt(token)