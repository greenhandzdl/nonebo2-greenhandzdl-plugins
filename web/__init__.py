from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入 requests, imgkit, nonebot_plugin_saa, tempfile 等模块
import requests
import imgkit
from nonebot_plugin_saa import MessageFactory, Image
import tempfile

# 定义一个命令处理器，响应用户输入的 "web" 指令，并且需要 @ 机器人
web_cmd = on_command("web", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@web_cmd.handle()
async def handle_web(bot: Bot, event: Event, state: T_State):
    # 获取用户输入的网页地址
    url = event.get_plaintext().strip()
    url = url.replace("/web", "").strip()
    # 如果没有输入地址，提示用户
    if not url:
        await bot.send(event, "请输入网页地址")
        return
    # 检查是否有协议头，如果没有，添加一个默认的 http
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    # 使用 requests 模块的 get 函数，获取网页的 html 内容，并设置超时时间为 10 秒
    try:
        response = requests.get(url, timeout=10)
        html = response.text
    except requests.exceptions.ConnectTimeout:
    # 如果连接超时，发送提示信息给用户，并结束命令处理
        await bot.send(event, "连接网页超时，请重试或换一个网址")
        await web_cmd.finish()
        return

    # 使用 imgkit 模块的 from_string 函数，将 html 内容转换为 png 图片，并保存到临时文件中
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp_file:
        imgkit.from_string(html, tmp_file.name)
    # 使用 MessageFactory 类构建消息，使用临时文件作为图片源
    msg = MessageFactory(Image(tmp_file.name))
    # 使用 bot 对象发送消息给用户，回复原消息并 @ 用户
    await web_cmd.send(msg, reply=True, at_sender=True)

    # 结束命令处理
    await web_cmd.finish()