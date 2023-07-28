# 导入nonebot2相关模块
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入随机数模块
import random

# 导入插件配置
from .config import Config

# 导入nonebot-plugin-send-anything-anywhere相关模块
from nonebot_plugin_saa import MessageFactory, Text


# 获取插件配置
global_config = Config()

# 定义一个命令处理器，响应用户输入的"random"或"随机数"指令，并且需要@机器人
random_cmd = on_command("random", aliases={"随机数"}, rule=to_me(), priority=5)

# 定义命令处理函数，生成一个1-10的随机数，并回复给用户
@random_cmd.handle()
async def handle_random(bot: Bot, event: Event, state: T_State):

    # 生成一个1-10的随机整数
    num = random.randint(global_config.random_dice_min, global_config.random_dice_max)

    # 构建一个消息对象，包含文字和at
    msg = MessageFactory([Text(f"你要的随机数是：{num}")])

    # 直接调用send方法在handler中回复消息，自动适配不同的adapter
    await msg.send(reply=True, at_sender=True)

    #结束命令处理
    await random_cmd.finish()