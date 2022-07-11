from typing import Generator, List, Optional, Union, Tuple, Dict, Any
from functools import cached_property, cmp_to_key
from dataclasses import dataclass
from collections import defaultdict

import jieba_fast.analyse
import threading
import pypinyin
import pymongo
import time
import random
import re
import atexit

from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from src.common.config import BotConfig

from ..repeater.model import ChatData

mongo_client = pymongo.MongoClient('127.0.0.1', 27017, w=0)

mongo_db = mongo_client['PallasBot']


memo_mongo = mongo_db['memo']
memo_mongo.create_index(name='keywords_index',
                           keys=[('keywords', pymongo.HASHED)])
memo_mongo.create_index(name='message_index',
                           keys=[('message', pymongo.HASHED)])
memo_mongo.create_index(name='insert_user_index',
                           keys=[('insert_user', pymongo.DESCENDING)])

class Memo:
    def __init__(self, data: Union[GroupMessageEvent, PrivateMessageEvent]):
        if (isinstance(data, GroupMessageEvent)):
            self.chat_data = ChatData(
                group_id=data.group_id,
                user_id=data.user_id,
                # 删除图片子类型字段
                raw_message=re.sub(
                    r',subType=\d+\]',
                    r']',
                    data.raw_message),
                plain_text=data.get_plaintext(),
                time=data.time,
                bot_id=data.self_id,
            )
            self.config = BotConfig(data.self_id, data.group_id)
        elif (isinstance(data, PrivateMessageEvent)):
            event_dict = data.dict()
            self.chat_data = ChatData(
                group_id=data.user_id,
                user_id=data.user_id,
                # 删除图片子类型字段
                raw_message=re.sub(
                    r',subType=\d+\]',
                    r']',
                    data.raw_message),
                plain_text=data.get_plaintext(),
                time=data.time,
                bot_id=data.self_id,
            )
            self.config = BotConfig(data.self_id, data.group_id)

    def insert_or_upgrade_data(self):
        group_id = self.chat_data.group_id
        user_id = self.chat_data.user_id
        raw_message = self.chat_data.raw_message

        # if '[CQ:' in self.chat_data.raw_message or len(self.chat_data.plain_text) == 0:
        #     return "没有记录捏"

        [first_str, second_str] = raw_message.split(" ", 1)
        first_str = first_str[4:]

        keywords_list = jieba_fast.analyse.extract_tags(first_str, topK=2)
        if len(keywords_list) < 2:
            keywords = self.chat_data.plain_text
        else:
            # keywords_list.sort()
            keywords = ' '.join(keywords_list)

        update_value = {
                '$set': {'message': second_str},
                '$set': {'insert_user': user_id}
            }
        memo_mongo.update_one({'keywords': keywords},update_value,upsert=True)

    def search_data(self) -> str:
        group_id = self.chat_data.group_id
        raw_message = self.chat_data.raw_message
        search_message = raw_message[4:]
        keywords_list = jieba_fast.analyse.extract_tags(search_message, topK=2)
        if len(keywords_list) < 2:
            keywords = self.chat_data.plain_text
        else:
            # keywords_list.sort()
            keywords = ' '.join(keywords_list)

        context = memo_mongo.find_one({'keywords': keywords})
        if not context:
            return "牛牛没有找到相关记录捏"
        else:
            return context["message"]
