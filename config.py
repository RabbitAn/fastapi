TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:123456@localhost:5432/postgres"
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default"
        }
    }
}


# -*- coding: utf-8 -*-
# TORTOISE_ORM = {
#     "connections": {
#         # 三要素：用户、密码、数据库名
#         "default": "postgres://postgres:123456@localhost:5432/postgres"
#     },
#     "apps": {
#         "models": {
#             "models": ["models", "aerich.models"],  # 模型 + 迁移表
#             "default_connection": "default",
#         }
#     },
#     "use_tz": True,
#     "timezone": "Asia/Shanghai",
# }