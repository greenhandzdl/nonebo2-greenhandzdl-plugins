from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

import markdown
import imgkit
from nonebot_plugin_saa import MessageFactory, Text, Image
import os
import datetime

man_cmd = on_command("man", rule=to_me(), priority=5)

@man_cmd.handle()
async def handle_man(bot: Bot, event: Event, state: T_State):
    param = event.get_plaintext().strip()
    param = param.replace("/man", "").strip()

    if not param:
        # 如果没有输入参数，使用默认的 README.md 文件
        md_file = "./src/plugins/README.md"
    else:
        # 否则，拼接成 ./src/plugins/<param>/README.md 文件
        md_file = f"./src/plugins/{param}/README.md"

    # 转换为绝对路径
    md_file = os.path.abspath(md_file)

    if not os.path.exists(md_file):
        # 检查文件是否存在，如果不存在，提示用户
        await bot.send(event, "没有找到对应的文件，请检查你输入的参数是否正确")
        return

    try:
        with open(md_file, "r", encoding="utf-8") as f:
            # 读取文件内容，并转换为 markdown 文本
            md_text = f.read()

        # 调用 markdown 模块的 markdown 函数，将 markdown 文本转换为 html 文本
        html_text = markdown.markdown(md_text)

        # 拼接成一个文件名
        file_name = f"{param}_manual.png"

        # 检查并创建 ./cookie 文件夹，如果不存在的话
        cookie_dir = "./cookie"
        if not os.path.exists(cookie_dir):
            os.mkdir(cookie_dir)

        # 拼接一个文件路径，使用 ./cookie 目录和文件名，并转换为绝对路径
        file_path = os.path.join(cookie_dir, file_name)
        file_path = os.path.abspath(file_path)

        # 调用 imgkit 模块的 from_string 函数，将 html 文本转换为 png 图片，并保存到文件路径中
        imgkit.from_string(html_text, file_path)

        with open(file_path, "rb") as f:
            # 读取文件路径中的字节数据
            image_data = f.read()

        # 使用MessageFactory类构建消息，并添加一些文本说明
        msg = MessageFactory([Text("这是我根据你输入的参数生成的说明：\n"), Image(image_data)])

        # 使用 bot 对象发送消息给用户，回复原消息并 @ 用户
        await msg.send(reply=True, at_sender=True)

    except Exception as e:
        # 如果出现异常，发送错误消息给用户
        await bot.send(event, f"处理命令时出现错误：{e}")

    # 结束命令处理
    await man_cmd.finish()