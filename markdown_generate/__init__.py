from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me


# 导入nonebot，markdown，imgkit，nonebot_plugin_saa，os和datetime模块
import markdown
import imgkit
import os
from pathlib import Path
import datetime 

# 导入nonebot-plugin-send-anything-anywhere相关模块
from nonebot_plugin_saa import MessageFactory, Text ,Image


# 定义一个命令处理器，响应用户输入的"md_generate"指令，并且需要@机器人
md_generate_cmd = on_command("md_generate", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@md_generate_cmd.handle()
async def handle_md_generate(bot: Bot, event: Event, state: T_State):
    # 获取用户输入的markdown文本
    md_text = event.get_plaintext().strip()
    md_text = md_text.replace("/md_generate", "").strip()
    # 如果没有输入文本，提示用户
    if not md_text:
        await bot.send(event, "请输入markdown文本")
        return
    # 调用markdown模块的markdown函数，将markdown文本转换为html文本
    html_text = markdown.markdown(md_text)
    # 获取发送者的用户信息和当前时间，并拼接成一个文件名
    user = event.sender # 直接获取用户信息
    user_id = event.user_id # 获取用户id
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # new
    file_name = f"{user.nickname}({user_id})_{current_time}.png" # new
    # 检查并创建 ./cookie 文件夹
    if not os.path.exists("./cookie"):
        os.makedirs("./cookie")
    # 拼接一个文件路径，使用./cookie目录和文件名，并转换为绝对路径
    file_path = Path("./cookie").joinpath(file_name).resolve()
    # 调用imgkit模块的from_string函数，将html文本转换为png图片，并保存到文件路径中
    imgkit.from_string(html_text, file_path)
    # 读取文件路径中的字节数据
    with open(file_path, "rb") as f:
        image_data = f.read()
    # 使用Image类的from_bytes方法创建图片消息段
    image_msg = Image.from_bytes(image_data)
    # 使用MessageFactory类构建消息
    msg = MessageFactory([Image(file_path),Text("这是渲染的图片")]) 
    # 使用bot对象发送消息给用户，回复原消息并@用户
    await msg.send(reply=True, at_sender=True)


    # 结束命令处理
    await md_generate_cmd.finish()