import requests
from requests.exceptions import RequestException
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot_plugin_saa import MessageFactory, Text
from .config import Config

global_config = Config()
gpt_cmd = on_command("gpt", rule=to_me(), priority=5)

@gpt_cmd.handle()
async def handle_gpt(bot: Bot, event: Event, state: T_State):
    try:
        # 获取用户输入的内容
        user_input = event.get_plaintext().strip()
        user_input = user_input.replace("/gpt", "").strip()

        # 构造请求的json数据
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

        # 提取回应内容中的回复
        reply_content = response_data["choices"][0]["message"]["content"]

        # 构造回复消息对象
        msg = MessageFactory([Text("主人～"), Text(reply_content), Text(" 喵～")])

        # 发送回复消息
        await msg.send(reply=True, at_sender=True)

    except RequestException as e:
        # 处理请求异常
        await bot.send(event, message="请求异常，请稍后再试")

    except Exception as e:
        # 处理其他异常
        await bot.send(event, message="发生了一些错误，请稍后再试")

    # 结束命令处理
    await gpt_cmd.finish()