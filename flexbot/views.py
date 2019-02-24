from flask import Flask, Blueprint, request
from .models import Trigger, Answer, Chat
from config import webhook_url, telegram_url
from typing import Dict
import requests
import logging
import random
import re
import itertools


flexbot = Blueprint('flexbot', __name__)


@flexbot.route(webhook_url, methods=['POST'])
def get_update():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        persist_chat(update['message']['chat'])
        send_random_triggered_answer(update['message'])

    return 'ok'


def persist_chat(chat: Dict):
    migrate_from = 'migrate_from_chat_id'
    migrate_to = 'migrate_to_chat_id'
    chat_has_migrated = (migrate_to in chat and migrate_from in chat)
    original_id = chat[migrate_from] if chat_has_migrated else chat['id']
    original_registry = Chat.query.filter(Chat.chat_id == original_id).first()

    if original_registry is None:
        Chat(title=chat['title'], chat_id=chat['id']).save()
    elif chat_has_migrated:
        original_registry.update(chat_id=chat[migrate_to])


def send_random_triggered_answer(message):
    chat_id = message['chat']['id']
    text = message['text']
    replies = get_triggered_replies(text, chat_id)
    if len(replies) > 0:
        return send_reply(random.choice(replies), chat_id)


def get_triggered_replies(text, chat_id):
    chat_triggers = Trigger.query\
        .filter(Trigger.chat_id == chat_id)\
        .all()
    answers_from_triggered = (
        (a.text for a in trigger.answers)
        for trigger in chat_triggers
        if re.search(trigger.expression, text) is not None
    )
    return list(itertools.chain(*answers_from_triggered))


def send_reply(reply, chat_id):
    response_url = f'{telegram_url}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': reply
    }
    return requests.post(response_url, json=payload)
