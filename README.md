1、首先安装fastapi：
pip install fastapi

2、创建一个文件，比如app.py，内容如下：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

3、运行uviicorn app:app --reload --host 0.0.0.0 --port 8000，启动服务
访问http://localhost:8000/，可以看到返回的Hello World。

4、如果需要添加路由，比如/users，可以这样写：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}
```

5、运行uviicorn app:app --reload --host 0.0.0.0 --port 8000，访问http://localhost:8000/users，可以看到返回的用户列表。
6、如果需要添加参数，比如/users/{user_id}，可以这样写：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

7、运行uviicorn app:app --reload --host 0.0.0.0 --port 8000，访问http://localhost:8000/users/123，可以看到返回的用户ID。
8、如果需要添加请求体，比如POST /users，可以这样写：

```python
from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users")
async def create_user(user: dict = Body(...)):
    return {"user": user}
```

9、运行uviicorn app:app --reload --host 0.0.0.0 --port 8000，使用POST方法，请求体格式为JSON，请求头中添加Content-Type: application/json，请求体中添加用户信息，比如{"name": "Alice"}，访问http://localhost:8000/users，可以看到返回的用户信息。 
10、如果需要添加响应体，比如GET /users/{user_id}，可以这样写：

```python
from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/users/{user_id}", response_model=dict)
async def get_user_v2(user_id: int):
    return {"user_id": user_id}
```

11、运行uviicorn app:app --reload --host 0.0.0.0 --port 8000，访问http://localhost:8000/users/123，可以看到返回的用户ID。

12、添加tortoiser-orm，可以用ORM来操作数据库
pip install tortoise-orm[aiosqlite]

13、添加配置文件，比如config.py，内容如下：

TORTOISE_ORM = {
    "connections": {
        "default": {
            "db_url": "mysql://root:123456@localhost:3306/fastapi_db",
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "123456",
                "database": "fastapi_db",
            },
        }
    },
    "apps": {
        "models": {
            "models": ["models.user", "aerich.models"],
            "default_connection": "default",
        }
    },
     "use_tz": False,  
     "timezone": "Asia/Shanghai",  //启用时区为上海
     "generate_schemas": True,
     
}


14、在app.py中导入配置，并初始化数据库：
```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
```

15、在models.py中定义数据库模型：

```python
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)


    class Meta:
        table = "users"
```

16、在app.py中添加路由，比如/users，可以这样写：

```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM
from models import User

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    users = await User.all()
    return {"users": [user.name for user in users]}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get(id=user_id)
    return {"user_id": user.id, "name": user.name}

@app.post("/users")
async def create_user(user: dict = Body(...)):
    new_user = await User.create(name=user["name"])
    return {"user_id": new_user.id, "name": new_user.name}

```
17、添加Aerich，可以用命令行工具来管理数据库
pip install aerich[fastapi]

18、数据库迁移，在项目根目录下运行命令：aerich init
aerich 命令
aerich migrate
aerich upgrade
aerich init -t config.TORTOISE_ORM
aerich init-db

19、添加equirements.txt，内容如下：
pip freeze > requirements.txt

20、挂载静态文件，比如在static目录下有个logo.png，可以这样写：

```python
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


21、添加jinja2模板，比如在templates目录下有个index.html，可以这样写：

```python
from fastapi import FastAPI, Body,Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

22、添加日志，比如在app.py中添加：

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

23、添加单元测试，比如在tests目录下有个test_main.py，可以这样写：

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == {"users": []}

def test_create_user():
    response = client.post("/users", json={"name": "Alice"})
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "name": "Alice"}
```
23、打包
requirements.txt 中同时写上 PyInstaller
pyinstaller
fastapi
uvicorn
# 其它依赖...
然后直接：
pip install -r requirements.txt
pyinstaller --onefile --noconsole main.py


