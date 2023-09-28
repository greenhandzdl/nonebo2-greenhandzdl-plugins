from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot_plugin_saa import MessageFactory, Text
from .config import repeatInt, repeatHitInt

message_handler = on_message()

@message_handler.handle()
async def repeat_message(bot: Bot, event: Event):
    user_input = event.get_plaintext().strip()

    if repeatInt >= repeatHitInt:
        repeat_text = Text(user_input)
        reply_message = MessageFactory.create([repeat_text])
        await bot.send(event, message=reply_message)