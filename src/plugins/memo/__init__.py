import random
import asyncio
import re
import time
import os
import threading

from nonebot import on_message, require, get_bot, logger, get_driver
from nonebot.exception import ActionFailed
from nonebot.typing import T_State
from nonebot.rule import keyword, to_me, Rule, startswith
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11 import permission
from nonebot.permission import Permission
from nonebot.permission import SUPERUSER
from src.common.config import BotConfig

from .memo import Memo


memo_insert_massage = on_message(
    rule=startswith("牛牛记录"),
    priority=6,
    block=True,
    permission=permission.GROUP
)

@memo_insert_massage.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    memo = Memo(event)
    memo.insert_or_upgrade_data()

memo_search_massage = on_message(
    rule=startswith("牛牛查询"),
    priority=6,
    block=True,
    permission=permission.GROUP
)

@memo_search_massage.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    memo = Memo(event)
    user_id = event.user_id
    group_id = event.group_id
    raw_message = event.raw_message
    response = memo.search_data()
    await get_bot(str(344713992)).call_api('send_group_msg', **{
        'message': response,
        'group_id': group_id
    })
    