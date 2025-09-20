from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
import asyncio
import os
import sys
from user import user_controller
from login import login_controller
from utils.system_info import system_monitor

app = FastAPI(title="Python系统监控", version="1.0.0")

# 数据库配置
DB_CONFIG = {
    "url": "postgres://postgres:123456@localhost:5432/postgres",
    "modules": {"models": ["models", "aerich.models"]},
    "generate_schemas": True,
    "add_exception_handlers": True
}

# 注册数据库
register_tortoise(app, **DB_CONFIG)

# 模板配置
base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
template = Jinja2Templates(directory=os.path.join(base_path, "templates"))

# 路由配置
@app.get("/")
async def root():
    return {"programStatus": "正在运行"}

@app.get("/page")
async def get_page(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    from utils.logger import system_logger
    client = f"{websocket.client.host}:{websocket.client.port}"
    system_logger.info(f"新的WebSocket连接: {client}")
    
    await websocket.accept()
    try:
        while True:
            data = system_monitor.get_system_info()
            await websocket.send_json(data)
            await asyncio.sleep(0.5)
    except Exception as e:
        system_logger.error(f"WebSocket连接关闭 ({client}): {str(e)}")
    finally:
        system_logger.info(f"WebSocket连接断开: {client}")

# 注册API路由
app.include_router(user_controller, prefix="/api", tags=["用户相关接口"])
app.include_router(login_controller, prefix="/api", tags=["登录相关接口"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
