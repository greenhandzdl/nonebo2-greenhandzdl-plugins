from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

import markdown
import imgkit
import os
from pathlib import Path
import datetime

from nonebot_plugin_saa import MessageFactory, Image

md_generate_cmd = on_command("md_generate", rule=to_me(), priority=5)

@md_generate_cmd.handle()
async def handle_md_generate(bot: Bot, event: Event, state: T_State):
    # 获取用户输入的markdown文本
    md_text = event.get_plaintext().strip()
    md_text = md_text.replace("/md_generate", "").strip()
    # 如果没有输入文本，提示用户
    if not md_text:
        await bot.send(event, "请输入markdown文本")
        return

    # 将markdown文本转换为html文本
    html_text = markdown.markdown(md_text)

    # 获取当前时间，并拼接成一个文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{current_time}.png"

    # 检查并创建 ./cookie 文件夹
    if not os.path.exists("./cookie"):
        os.makedirs("./cookie")

    # 拼接一个文件路径，使用./cookie目录和文件名，并转换为绝对路径
    file_path = Path("./cookie").joinpath(file_name).resolve()

    # 将html文本转换为png图片，并保存到文件路径中
    imgkit.from_string(html_text, str(file_path), options={"format": "png"})

    # 读取文件路径中的字节数据
    with open(file_path, "rb") as f:
        image_data = f.read()

    # 使用MessageFactory类构建消息，将图片数据转换为Image对象
    msg = MessageFactory(Image.from_bytes(image_data))

    # 使用bot对象发送消息给用户，回复原消息并@用户
    await msg.send(bot, event)

    # 结束命令处理
    await md_generate_cmd.finish()