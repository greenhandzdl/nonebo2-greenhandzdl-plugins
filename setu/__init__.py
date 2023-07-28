# 导入nonebot2相关模块
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入requests模块，用于发送http请求
import requests

# 导入json模块，用于解析json数据
import json


# 导入插件配置
from .config import Config

# 导入nonebot-plugin-send-anything-anywhere相关模块
from nonebot_plugin_saa import MessageFactory, Text ,Image

# 获取插件配置实例
global_config = Config()

# 定义一个命令处理器，响应用户输入的"setu"指令，并且需要@机器人
setu_cmd = on_command("setu", rule=to_me(), priority=5)

@setu_cmd.handle()
async def handle_gpt(bot: Bot, event: Event, state: T_State):
    # 向目标网址发送get请求，获取响应对象
    response = requests.get(global_config.setu_link)

    # 从响应对象中提取文本内容
    response_text = response.text

    # 将文本内容转换为字典对象，使用json模块的loads方法
    response_dict = json.loads(response_text)

    # 从字典对象中提取url键对应的值
    response_url = response_dict["url"]

    # 构建一个消息对象，包含文字和at
    msg = MessageFactory([Image(response_url),Text("这是你要的涩图，杂鱼～")])

    # 直接调用send方法在handler中回复消息，自动适配不同的adapter
    await msg.send(reply=True, at_sender=True)

    # 结束命令处理
    await setu_cmd.finish()