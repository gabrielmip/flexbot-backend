from flask import Flask, Blueprint, request
from typing import Dict
import requests
import logging
import random
import hashlib
import re
import itertools

from .models import Trigger, Answer, Chat, AccessToken
from config import webhook_url, telegram_url, config_panel_url
from misc import flatten


bot = Blueprint('bot', __name__)


@bot.route(webhook_url, methods=['POST'])
def get_update():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        chat = update['message']['chat']
        text = update['message']['text']

        persist_chat(chat)
        if is_command(update['message']):
            process_command(text, chat['id'])
        else:
            send_random_triggered_reply(text, chat['id'])

    return 'ok'


def persist_chat(chat: Dict):
    migrate_from = 'migrate_from_chat_id'
    migrate_to = 'migrate_to_chat_id'
    chat_has_migrated = (migrate_to in chat and migrate_from in chat)
    original_id = chat[migrate_from] if chat_has_migrated else chat['id']
    original_registry = Chat.query.filter(Chat.chat_id == original_id).first()
    title = None if 'title' not in chat else chat['title']

    if original_registry is None:
        Chat(title=title, chat_id=chat['id']).save()
    else:
        if chat_has_migrated:
            original_registry.update(chat_id=chat[migrate_to])
        if original_registry.title != title:
            original_registry.update(title=title)


def is_command(message):
    if 'entities' not in message:
        return False
    else:
        entity_types = map(lambda e: e['type'], message['entities'])
        return any([etype == 'bot_command' for etype in entity_types])


def process_command(command, chat_id):
    if command == '/config':
        message = get_chat_config_message(chat_id)
        send_reply(message, chat_id)


def get_chat_config_message(chat_id):
    token = get_chat_config_access_token(chat_id)
    AccessToken(chat_id=chat_id, token=token).save()
    url = f'{config_panel_url}/{token}'
    return f'Go to the configuration panel by clicking [this link]({url}).'


def get_chat_config_access_token(chat_id):
    token_length = 25
    seed = str(random.random()).encode('ascii')
    token = hashlib.sha256(seed).hexdigest()[:token_length]
    return token


def send_random_triggered_reply(text, chat_id):
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
    return list(flatten(answers_from_triggered))


def send_reply(reply, chat_id):
    response_url = f'{telegram_url}/sendMessage'
    params = {
        'parse_mode': 'markdown'
    }
    payload = {
        'chat_id': chat_id,
        'text': reply
    }
    return requests.post(response_url, json=payload, params=params)
