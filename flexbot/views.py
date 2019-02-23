from flask import Flask, Blueprint, request
from .models import Trigger, Answer
from utils import dict_to_object
import requests
import logging
import random
import re
import itertools


flexbot = Blueprint('flexbot', __name__)
token = ''


@flexbot.route('/update', methods=['POST'])
def get_update():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        replies = get_triggered_replies(text, chat_id)
        if len(replies) > 0:
            chosen_reply = random.choice(replies)
            reply_response = send_reply(chosen_reply, chat_id)
            return str(reply_response.status_code)

    return 'ok'


@flexbot.route('/fake-receiver', methods=["POST"])
def fake_receiver():
    print(request.get_json())
    return 'ok'


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
    response_url = 'http://localhost:5000/flexbot/fake-receiver'
    payload = {
        'chat_id': chat_id,
        'text': reply
    }
    return requests.post(response_url, json=payload)
