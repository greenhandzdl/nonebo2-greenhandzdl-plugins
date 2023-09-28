import os
import subprocess
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot_plugin_saa import MessageFactory, Text

from .config import Config

update_cmd = on_command("update", rule=to_me(), priority=5)

@update_cmd.handle()
async def handle_update(bot: Bot, event: Event, state: T_State):
    current_dir = os.getcwd()
    os.chdir(os.path.join(current_dir, "src", "plugins"))
    
    # 执行git pull命令
    output = subprocess.getoutput("git pull")
    
    # 判断是否有更新
    if "Already up to date" in output:
        msg = MessageFactory(Text("插件无更新"))
    else:
        # 获取最新的commit信息
        commit_output = subprocess.getoutput("git log -1 --pretty=format:'%h - %s (%cr)'")
        msg = MessageFactory(Text(f"插件已更新！\n最新的commit信息：\n{commit_output}"))
    
    os.chdir(current_dir)
    await msg.send(reply=True, at_sender=True)
    await update_cmd.finish()