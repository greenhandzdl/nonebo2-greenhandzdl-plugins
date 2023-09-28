from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
import markdown
import imgkit
from nonebot_plugin_saa import MessageFactory, Text, Image
import os

man_cmd = on_command("man", rule=to_me(), priority=5)

@man_cmd.handle()
async def handle_man(bot: Bot, event: Event, state: T_State):
    param = event.get_plaintext().strip().replace("/man", "").strip()
    md_file = f"./src/plugins/{param}/README.md" if param else "./src/plugins/README.md"
    md_file = os.path.abspath(md_file)

    if not os.path.exists(md_file):
        await bot.send(event, "没有找到对应的文件，请检查你输入的参数是否正确")
        return

    try:
        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()
        html_text = markdown.markdown(md_text)
        file_name = f"{param}_manual.png"
        cookie_dir = "./cookie"
        if not os.path.exists(cookie_dir):
            os.mkdir(cookie_dir)
        file_path = os.path.join(cookie_dir, file_name)
        file_path = os.path.abspath(file_path)
        imgkit.from_string(html_text, file_path)

        with open(file_path, "rb") as f:
            image_data = f.read()

        msg = MessageFactory([Text("这是我根据你输入的参数生成的说明：\n"), Image(image_data)])
        await msg.send(reply=True, at_sender=True)

    except Exception as e:
        await bot.send(event, f"处理命令时出现错误：{e}")

    await man_cmd.finish()