# 导入nonebot2相关模块
from pydantic import BaseSettings

# 定义插件配置类
class Config(BaseSettings):
    # 随机数最小值，默认为1
    random_dice_min: int = 1
    # 随机数最大值，默认为10
    random_dice_max: int = 10

global_config = Config()
