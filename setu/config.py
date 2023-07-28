# 导入nonebot2相关模块
from pydantic import BaseSettings

# 定义插件配置类
class Config(BaseSettings):
    setu_link :str = "https://api.likepoems.com/img/pixiv/?type=json"

# 获取插件配置实例
global_config = Config()