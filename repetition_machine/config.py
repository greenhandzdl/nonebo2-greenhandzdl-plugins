# 导入nonebot2相关模块
from pydantic import BaseSettings


class Config(BaseSettings):
    """Plugin Config Here"""
    repeatInt : int = 100
    repeatHitInt : int = 40