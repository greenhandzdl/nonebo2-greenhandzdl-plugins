# 导入nonebot2相关模块
from pydantic import BaseSettings

# 定义插件配置类
class Config(BaseSettings):
    # 模型名称，默认为"rwkv"
    model: str = "rwkv"
    # 是否流式处理，默认为False
    stream: bool = False
    # 最大生成的token数，默认为1000
    max_tokens: int = 1000
    # 温度参数，默认为1.2
    temperature: float = 1.2
    # top_p参数，默认为0.5
    top_p: float = 0.5
    # presence_penalty参数，默认为0.4
    presence_penalty: float = 0.4
    # frequency_penalty参数，默认为0.4
    frequency_penalty: float = 0.4

# 获取插件配置实例
global_config = Config()