from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入 markdown, imgkit, nonebot_plugin_saa, os, datetime 等模块
import markdown
import imgkit
from nonebot_plugin_saa import MessageFactory, Text, Image
import os
import datetime

# 定义一个命令处理器，响应用户输入的 "man" 指令，并且需要 @ 机器人
man_cmd = on_command("man", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@man_cmd.handle()
async def handle_man(bot: Bot, event: Event, state: T_State):

    # 获取用户输入的参数
    param = event.get_plaintext().strip()
    param = param.replace("/man", "").strip()

    # 如果没有输入参数，使用默认的 README.md 文件
    if not param:
        md_file = "../src/plugins/README.md"

    # 否则，拼接成 ../src/plugins/<param>/README.md 文件
    else:
        md_file = f"../src/plugins/{param}/README.md"

    # 检查文件是否存在，如果不存在，提示用户
    if not os.path.exists(md_file):
        await bot.send(event, "没有找到对应的文件，请检查你输入的参数是否正确")
        return

    # 读取文件内容，并转换为 markdown 文本
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 调用 markdown 模块的 markdown 函数，将 markdown 文本转换为 html 文本
    html_text = markdown.markdown(md_text)

    # 获取发送者的 id 和当前时间，并拼接成一个文件名
    sender_id = event.sender.user_id
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{param}_manual.png"

    # 检查并创建 ./cookie 文件夹，如果不存在的话
    cookie_dir = "./cookie"
    if not os.path.exists(cookie_dir):
        os.mkdir(cookie_dir)

    # 拼接一个文件路径，使用 ./cookie 目录和文件名，并转换为绝对路径
    file_path = os.path.join(cookie_dir, file_name)

    # 调用 imgkit 模块的 from_string 函数，将 html 文本转换为 png 图片，并保存到文件路径中
    imgkit.from_string(html_text, file_path)

    # 使用 MessageFactory 类构建消息，使用文件路径作为图片源，并添加一些文本说明
    msg = MessageFactory([Text("这是我根据你输入的参数生成的说明："), Image(file_path)])

    # 使用 bot 对象发送消息给用户，回复原消息并 @ 用户
    await msg.send(reply=True, at_sender=True)

    # 结束命令处理
    await man_cmd.finish()
