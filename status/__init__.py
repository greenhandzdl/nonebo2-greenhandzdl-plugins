# 导入nonebot2相关模块
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

import platform
import psutil
import requests
import subprocess
import time


# 导入插件配置
from .config import Config

# 导入nonebot-plugin-send-anything-anywhere相关模块
from nonebot_plugin_saa import MessageFactory, Text ,Image

# 获取插件配置实例
global_config = Config()

# 定义一个命令处理器，响应用户输入的"status"指令，并且需要@机器人
status_cmd = on_command("status", rule=to_me(), priority=5)

def get_sysinfo():
    sysinfo = {}
    sysinfo['OS'] = platform.system()  # 获取操作系统类型
    sysinfo['Host'] = platform.node()  # 获取主机名
    sysinfo['Kernel'] = platform.release()  # 获取内核版本
    sysinfo['Uptime'] = format_timespan(psutil.boot_time())  # 获取系统运行时间
    sysinfo['CPU'] = get_cpu_model()  # 获取CPU型号
    sysinfo['Memory'] = format_size(psutil.virtual_memory().total)  # 获取内存大小
    return sysinfo

def get_cpu_model():
    try:
        output = subprocess.check_output(['lscpu'], stderr=subprocess.STDOUT).decode('utf-8')  # 执行命令获取CPU信息
        lines = output.split('\n')
        for line in lines:
            if line.startswith('Model name:'):
                return line.split(':', 1)[1].strip()  # 提取CPU型号信息
        return ''
    except subprocess.CalledProcessError as e:
        print(e)
        return ''

def get_yiyan():
    try:
        response = requests.get('https://v1.hitokoto.cn')  # 发送HTTP请求获取一言
        data = response.json()
        return data.get('hitokoto', '')  # 提取一言内容
    except requests.RequestException as e:
        print(e)
        return None

def format_size(size):
    power = 2**10
    n = 0
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"  # 格式化文件大小

def format_timespan(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"  # 格式化时间间隔

def get_output():
    cat = '''
       /\_/\\
      ( o.o )
       > ^ <
    '''
    
    yiyan = get_yiyan()
    if yiyan is not None:
        yiyan_output = "一言: {}".format(yiyan)  # 格式化一言输出
    
    current_unix_time = time.time()
    current_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
    time_output = "当前的Unix时间戳: {}\n当前时间:         {}".format(current_unix_time, current_time)  # 格式化时间输出
    
    sysinfo = get_sysinfo()
    if sysinfo is not None:
        sysinfo_output = "系统信息:\n操作系统:       {}\n主机名:         {}\n内核版本:       {}\n系统运行时间:   {}\nCPU型号:        {}\n内存大小:       {}".format(
            sysinfo.get('OS', ''),
            sysinfo.get('Host', ''),
            sysinfo.get('Kernel', ''),
            sysinfo.get('Uptime', ''),
            sysinfo.get('CPU', ''),
            sysinfo.get('Memory', '')
        )  # 格式化系统信息输出
    
    output = "{}\n{}\n{}".format(cat, yiyan_output, sysinfo_output)  # 将输出内容拼接到一起
    return output  # 返回输出内容

@status_cmd.handle()
async def handle_gpt(bot: Bot, event: Event, state: T_State):

    # 构建一个消息对象，包含文字和at
    msg = MessageFactory([Text(get_output())])

    # 直接调用send方法在handler中回复消息，自动适配不同的adapter
    await msg.send(reply=True, at_sender=True)

    # 结束命令处理
    await status_cmd.finish()