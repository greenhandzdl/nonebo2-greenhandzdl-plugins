from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot_plugin_saa import MessageFactory, Text

message_handler = on_message()

@message_handler.handle()
async def repeat_message(bot: Bot, event: Event):
    user_input = event.get_plaintext().strip()

    # 在 __init__ 函数中定义变量
    repeatInt = 100
    repeatHitInt = 40

    # 将变量存储在 plugin_config 中
    plugin_config =  {
        "repeatInt": repeatInt,
        "repeatHitInt": repeatHitInt
    }

    if repeatInt >= repeatHitInt:
        repeat_text = str(user_input)
        reply_message = MessageFactory(Text(repeat_text))
        await bot.send(event, message=reply_message)