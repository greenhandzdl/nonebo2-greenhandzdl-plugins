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
    md_text = event.get_plaintext().strip().replace("/md_generate", "").strip()
    if not md_text:
        await bot.send(event, "请输入markdown文本")
        return

    html_text = markdown.markdown(md_text)
    #current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #file_name = f"{current_time}.png"
    file_name = f"md_generate_cookies.png"
    file_path =  os.path.join("./cookie", file_name)
    file_path = os.path.abspath(file_path)

    try:
        imgkit.from_string(html_text, file_path)
        with open(file_path, "rb") as f:
            image_data = f.read()
        msg = MessageFactory(Image(image_data))
        await msg.send(bot, event)
    except Exception as e:
        await bot.send(event, f"生成图片时出现错误：{e}")
        return

    await md_generate_cmd.finish()
