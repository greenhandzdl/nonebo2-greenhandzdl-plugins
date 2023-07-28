from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

# 导入 requests, imgkit, nonebot_plugin_saa, tempfile, os 等模块
import requests
import imgkit
from nonebot_plugin_saa import MessageFactory, Image
import tempfile
import os

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

    # 使用 requests.head 函数先检查网页地址是否有效，如果返回状态码不是 200，就不要继续请求网页内容
    try:
        head_response = requests.head(url, timeout=10)
        if head_response.status_code != 200:
            await bot.send(event, "网页地址无效，请重试或换一个网址")
            await web_cmd.finish()
            return
    except requests.exceptions.RequestException as e:
        #如果出现任何请求异常，发送提示信息给用户，并结束命令处理
        await bot.send(event, f"请求网页失败，错误信息：{e}")
        await web_cmd.finish()
        return

    #使用 requests 模块的 get 函数，获取网页的 html 内容，并设置超时时间为 20 秒
    try:
        response = requests.get(url, timeout=20)
        html = response.text
    except requests.exceptions.RequestException as e:

        #如果出现任何请求异常，发送提示信息给用户，并结束命令处理
        await bot.send(event, f"获取网页内容失败，错误信息：{e}")
        await web_cmd.finish()
        return

    # 使用 imgkit 模块的 from_string 函数，将 html 内容转换为 png 图片，并保存到 ./cookie 文件夹中，使用网站链接的域名作为图片文件的名字
    # 创建 ./cookie 文件夹，如果不存在的话
    cookie_dir = "./cookie"
    if not os.path.exists(cookie_dir):
        os.mkdir(cookie_dir)

    # 提取网站链接的域名部分，去掉协议头和斜杠
    domain = url.split("//")[-1].split("/")[0]

    # 将 . 替换为 _
    domain = domain.replace(".", "_")

    # 拼接图片文件的路径和名字，使用 png 格式
    image_path = os.path.join(cookie_dir, domain + ".png")

    # 将 html 内容转换为 png 图片，并保存到图片文件中
    imgkit.from_string(html, image_path)

    # 使用 MessageFactory 类构建消息，使用图片文件作为图片源，并转换为 nonebot2 的 MessageSegment 类
    msg = MessageFactory(Image(image_path))

    # 使用 bot 对象发送消息给用户，回复原消息并 @ 用户
    await msg.send(reply=True, at_sender=True)

    # 结束命令处理
    await web_cmd.finish()