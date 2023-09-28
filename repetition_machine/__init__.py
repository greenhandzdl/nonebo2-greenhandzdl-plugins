from nonebot import on_message, get_driver
from nonebot.adapters import Bot, Event
from nonebot_plugin_saa import MessageFactory, Text
from pydantic import BaseModel
from config import repeatInt, repeatHitInt

class Config(BaseModel):
    repeatInt: int = repeatInt
    repeatHitInt: int = repeatHitInt

global_config = get_driver().config
config = Config()

message_handler = on_message()

@message_handler.handle()
async def repeat_message(bot: Bot, event: Event):
    # 获取用户发送的消息内容
    user_input = event.get_plaintext().strip()

    # 获取配置文件中的值
    repeat_int = config.repeatInt
    repeat_hint_int = config.repeatHitInt

    # 判断是否满足复读条件
    if repeat_int >= repeat_hint_int:
        # 构造复读消息
        repeat_text = Text(user_input)

        # 使用MessageFactory构造消息
        reply_message = MessageFactory.create()
        reply_message.append(repeat_text)

        # 发送回复消息
        await bot.send(event, message=reply_message)