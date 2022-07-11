import random
import asyncio
import re
import time
import os
import threading

from nonebot import on_message, require, get_bot, logger, get_driver
from nonebot.exception import ActionFailed
from nonebot.typing import T_State
from nonebot.rule import keyword, to_me, Rule,startswith
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11 import permission
from nonebot.permission import Permission
from nonebot.permission import SUPERUSER
from src.common.config import BotConfig

from .nlp import NlpChat

nlp_chat_massage = on_message(
    rule=startswith("牛牛"),
    priority=16,
    block=True,
    permission=permission.GROUP
)

@nlp_chat_massage.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    nlp_chat= NlpChat()
    message_id = event.message_id
    group_id = event.group_id
    raw_message = event.raw_message
    response = nlp_chat.get_response(raw_message[2:])
    await get_bot(str(344713992)).call_api('send_group_msg', **{
        'message': response,
        'group_id': group_id
    })
    # if event.raw_message[0]=="牛":
    #     await get_bot(str(344713992)).call_api('send_group_msg', **{
    #         'message': "牛牛正在汪sir办公室听讲座",
    #         'group_id': 719244062
    #     })
