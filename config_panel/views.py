from flask import (
    Blueprint,
    render_template,
    jsonify,
    json,
    request,
    redirect,
    url_for)
from models import AccessToken, TriggerGroup, Trigger, Answer
from .forms.edit_trigger import EditTrigger


config_panel = Blueprint(
    'config_panel',
    __name__,
    template_folder='templates',
    static_folder='static')


@config_panel.route('/<received_token>')
def get_chat_associated_to_token(received_token):
    access_token = AccessToken.find(received_token)
    if access_token is None:
        return "Invalid token", 401

    return jsonify(access_token.chat.to_dict())


@config_panel.route('/trigger_groups', methods=['post'])
@config_panel.route('/trigger_groups/<trigger_group_id>', methods=['put'])
def edit_trigger_group(trigger_group_id=None):
    received_token = request.headers.get('Authorization')
    access_token = AccessToken.find(received_token)
    if access_token is None:
        return "Invalid token", 401

    trigger_group = (TriggerGroup(chat_id=access_token.chat_id)
        if trigger_group_id is None
        else TriggerGroup.query.get(trigger_group_id))

    if trigger_group is None:
        return "Not found", 404
    
    if trigger_group.chat_id != access_token.chat_id:
        return "Forbidden", 403

    group_attrs = request.get_json()
    trigger_group.update(ignore_case=group_attrs['ignore_case'], ignore_repeated_letters=group_attrs['ignore_repeated_letters'])
    update_trigger_group_attrs(trigger_group, group_attrs['answers'], group_attrs['triggers'])

    return "saved"


@config_panel.route('/trigger_groups/<trigger_group_id>', methods=['delete'])
def delete_trigger_group(trigger_group_id):
    token = request.headers.get('Authorization')
    access_token = AccessToken.find(token)
    trigger_group = TriggerGroup.query.get(trigger_group_id)

    if access_token is None:
        return "Invalid", 401

    if trigger_group is None:
        return "Not found", 404

    if trigger_group.chat_id != access_token.chat_id:
        return "Forbidden", 403
    
    delete_answers(trigger_group)
    delete_triggers(trigger_group)
    trigger_group.delete()

    return "deleted"


def update_trigger_group_attrs(trigger_group, updated_answers, updated_triggers):
    update_answers(trigger_group, updated_answers)
    update_triggers(trigger_group, updated_triggers)


def update_answers(trigger_group, new_answers):
    delete_answers(trigger_group)
    for new_answer in new_answers:
        Answer(text=new_answer['text'], trigger_group_id=trigger_group.trigger_group_id).save()


def delete_answers(trigger_group):
    for current_answer in trigger_group.answers:
        current_answer.delete()

    
def update_triggers(trigger_group, new_triggers):
    delete_triggers(trigger_group)
    for new_trigger in new_triggers:
        Trigger(expression=new_trigger['expression'], trigger_group_id=trigger_group.trigger_group_id).save()


def delete_triggers(trigger_group):
    for current_trigger in trigger_group.triggers:
        current_trigger.delete()
    