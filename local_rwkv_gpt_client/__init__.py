# 导入nonebot2相关模块
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入requests模块，用于发送http请求
import requests

# 导入插件配置
from .config import Config

# 导入nonebot-plugin-send-anything-anywhere相关模块
from nonebot_plugin_saa import MessageFactory, Text

# 获取插件配置实例
global_config = Config()

# 定义一个命令处理器，响应用户输入的"gpt"指令，并且需要@机器人
gpt_cmd = on_command("gpt", rule=to_me(), priority=5)

# 定义命令处理函数，向127.0.0.1:8000发送一个json数据，并回复给用户
@gpt_cmd.handle()
async def handle_gpt(bot: Bot, event: Event, state: T_State):

    # 获取用户的输入内容，去掉"gpt"前缀
    user_input = event.get_plaintext().strip()
    user_input = user_input.replace("/gpt", "").strip()

    #构造json数据，将用户的输入放入messages的content中，其他字段使用插件配置的属性值
    json_data = {
        "messages": [
        {
            "role": "user",
            "content": user_input
        }
        ],
        "model": global_config.model,
        "stream": global_config.stream,
        "max_tokens": global_config.max_tokens,
        "temperature": global_config.temperature,
        "top_p": global_config.top_p,
        "presence_penalty": global_config.presence_penalty,
        "frequency_penalty": global_config.frequency_penalty
    }

    # 发送http请求，获取回应内容
    response = requests.post("http://127.0.0.1:8000/chat/completions", json=json_data)
    response_data = response.json()

    # 提取回应内容中的content字段
    reply_content = response_data["choices"][0]["message"]["content"]

    # 构建一个消息对象，包含文字和at
    msg = MessageFactory([Text("主人～"), Text(reply_content), Text(" 喵～")])

    # 直接调用send方法在handler中回复消息，自动适配不同的adapter
    await msg.send(reply=True, at_sender=True)

    # 结束命令处理
    await gpt_cmd.finish()