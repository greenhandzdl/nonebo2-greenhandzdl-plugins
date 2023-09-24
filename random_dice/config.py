# 导入nonebot2相关模块
from pydantic import BaseSettings

# 定义插件配置类
class Config(BaseSettings):
    # 限制一次性随机多少
    random_max_count = 3

global_config = Config()
