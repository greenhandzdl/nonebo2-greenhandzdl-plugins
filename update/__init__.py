import os
import subprocess
import time
from nonebot import on_command, get_driver
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
        msg = MessageFactory(Text("无更新"))
    else:
        # 获取最新的commit信息
        commit_output = subprocess.getoutput("git log -1 --pretty=format:'%h - %s (%cr)'")
        msg = MessageFactory(Text(f"插件已更新！\n最新的commit信息：\n{commit_output}"))
        
        # 发送消息给用户
        await msg.send(reply=True, at_sender=True)
        
        # 延迟一段时间后重启机器人
        time.sleep(3)
        restart_bot()
    
    os.chdir(current_dir)
    await update_cmd.finish()

def restart_bot():
    # 获取机器人的配置
    global_config = get_driver().config
    config = Config.parse_obj(global_config)
    
    # 重启机器人
    os.execv(config.cli_path, [config.cli_path, *config.cli_args])