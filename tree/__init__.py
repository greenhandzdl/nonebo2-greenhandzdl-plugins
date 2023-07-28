# 导入nonebot-plugin-saa模块
import os
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot_plugin_saa import MessageFactory, Text

# 导入seedir模块
import seedir as sd
import io
import sys


# 定义一个命令处理器，响应用户输入的"tree"指令，并且需要@机器人
tree_cmd = on_command("tree", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@tree_cmd.handle()
async def handle_tree(bot: Bot, event: Event, state: T_State):
    # 调用os模块的getcwd()方法，获取当前工作目录
    plugin_dir = os.getcwd() + "/src/plugins"
    # 创建一个StringIO对象
    result = io.StringIO()
    # 保存原来的标准输出
    old_stdout = sys.stdout
    # 将标准输出设置为StringIO对象
    sys.stdout = result
    # 调用sd.seedir()函数，打印文件树
    sd.seedir(plugin_dir, style="lines", depthlimit=1, exclude_folders=".git")
    # 恢复原来的标准输出
    sys.stdout = old_stdout
    # 获取StringIO对象中的字符串
    result_string = result.getvalue()
    # 关闭StringIO对象
    result.close()

    # 使用MessageFactory和Text类构建消息
    msg = MessageFactory(Text(result_string))
    # 使用send方法发送消息给用户
    await msg.send(reply=True, at_sender=True)
    # 结束命令处理
    await tree_cmd.finish()