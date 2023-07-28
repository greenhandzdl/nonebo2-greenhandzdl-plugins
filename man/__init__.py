from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入 markdown, imgkit, nonebot_plugin_saa, os, datetime 等模块

import markdown
import imgkit
from nonebot_plugin_saa import MessageFactory, Text, Image
import os

# 定义一个命令处理器，响应用户输入的 "man" 指令，并且需要 @ 机器人
man_cmd = on_command("man", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@man_cmd.handle()
async def handle_man(bot: Bot, event: Event, state: T_State):
    # 获取用户输入的参数，如果没有输入参数，使用默认的 README.md 文件
    param = event.get_plaintext().strip().replace("/man", "").strip() or "README"

    # 拼接成 ./src/plugins/<param>/README.md 文件，并转换为绝对路径
    md_file = os.path.abspath(f"./src/plugins/{param}/README.md")

    # 检查文件是否存在，如果不存在，提示用户并结束命令处理
    if not os.path.exists(md_file):
        await bot.send(event, "没有找到对应的文件，请检查你输入的参数是否正确")
        return await man_cmd.finish()

    # 读取文件内容，并转换为 markdown 文本和 html 文本
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
    html_text = markdown.markdown(md_text)

    # 拼接成一个文件名和文件路径，使用 ./cookie 目录和文件名，并转换为绝对路径
    file_name = f"{param}_manual.png"
    file_path = os.path.abspath(os.path.join("./cookie", file_name))

    # 检查并创建 ./cookie 文件夹，如果不存在的话
    os.makedirs("./cookie", exist_ok=True)

    # 将 html 文本转换为 png 图片，并保存到文件路径中
    imgkit.from_string(html_text, file_path)

    # 读取文件路径中的字节数据，并创建图片消息段
    with open(file_path, "rb") as f:
        image_data = f.read()
    image_msg = Image(image_data)

    # 构建消息，并添加一些文本说明
    msg = MessageFactory([Text("这是我根据你输入的参数生成的说明：\n"), image_msg])

    # 发送消息给用户，回复原消息并 @ 用户，并结束命令处理
    await msg.send(reply=True, at_sender=True)
    await man_cmd.finish()