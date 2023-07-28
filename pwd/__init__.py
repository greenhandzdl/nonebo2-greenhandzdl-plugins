# 导入nonebot-plugin-saa模块
import os
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot_plugin_saa import MessageFactory, Text

# 定义一个命令处理器，响应用户输入的"pwd"指令，并且需要@机器人
pwd_cmd = on_command("pwd", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@pwd_cmd.handle()
async def handle_pwd(bot: Bot, event: Event, state: T_State):
    # 调用os模块的getcwd()方法，获取当前工作目录
    cwd = os.getcwd()
    # 使用MessageFactory和Text类构建消息
    msg = MessageFactory(Text(cwd))
    # 使用send方法发送消息给用户
    await msg.send(reply=True, at_sender=True)
    # 结束命令处理
    await pwd_cmd.finish()