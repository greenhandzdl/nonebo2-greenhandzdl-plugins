# 导入nonebot-plugin-saa模块
import os
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot_plugin_saa import MessageFactory, Text

from .config import Config

# global_config = get_driver().config
# config = Config.parse_obj(global_config)

# 定义一个命令处理器，响应用户输入的"about"指令，并且需要@机器人
about_cmd = on_command("about", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@about_cmd.handle()
async def handle_about(bot: Bot, event: Event, state: T_State):
    # 使用MessageFactory和Text类构建消息
    msg = MessageFactory(Text("这是项目地址：https://github.com/greenhandzdl/nonebo2-greenhandzdl-plugins"))
    # 使用send方法发送消息给用户
    await msg.send(reply=True, at_sender=True)
    # 结束命令处理
    await about_cmd.finish()