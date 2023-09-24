from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

import random

random_cmd = on_command("random", rule=to_me(), priority=5, aliases={"随机"})

@random_cmd.handle()
async def handle_random(bot: Bot, event: Event, state: T_State):
    param = event.get_plaintext().strip()
    param = param.replace("/random", "").strip()
    param = param.replace("/随机", "").strip()

    # 判断是否有参数
    if not param:
        min_value = 1
        max_value = 100
        throw_count = 1
    else:
        # 提取最小值、最大值和投掷次数
        try:
            min_value, max_value, throw_count = map(int, param.split())
        except ValueError:
            await bot.send(event, "参数格式不正确，请输入整数值")
            return

    # 检查投掷次数是否超过限制
    if throw_count > 10:
        await bot.send(event, "投掷次数不能超过10")
        return

    # 生成随机数
    msg = ""
    for i in range(throw_count):
        random_number = random.randint(min_value, max_value)
        msg += f"第{i+1}次，你投出的点数为：{random_number}\n"

    # 发送消息给用户
    await bot.send(event, msg)
