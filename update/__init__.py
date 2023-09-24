import os
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot_plugin_saa import MessageFactory, Text

from .config import Config

# global_config = get_driver().config
# config = Config.parse_obj(global_config)

# 定义一个命令处理器，响应用户输入的"update"指令，并且需要@机器人
update_cmd = on_command("update", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@update_cmd.handle()
async def handle_update(bot: Bot, event: Event, state: T_State):
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 切换到插件目录
    os.chdir(os.path.join(current_dir, "src", "plugins"))
    # 执行git pull命令
    os.system("git pull")
    # 切换回原来的工作目录
    os.chdir(current_dir)

    # 使用MessageFactory和Text类构建消息
    msg = MessageFactory(Text("插件已更新！"))
    # 使用send方法发送消息给用户
    await msg.send(reply=True, at_sender=True)
    # 结束命令处理
    await update_cmd.finish()