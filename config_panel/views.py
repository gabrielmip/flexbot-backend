from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for)
from bot.models import AccessToken, Trigger, Answer
from .forms.edit_trigger import EditTrigger


config_panel = Blueprint(
    'config_panel',
    __name__,
    template_folder='templates',
    static_folder='static')


@config_panel.route('/')
def list_triggers():
    received_token = request.args.get('token')
    if received_token is None:
        return render_template('invalid_token.html')

    access_token = AccessToken.find(received_token)
    if access_token is None:
        return render_template('invalid_token.html'), 401

    return render_template(
        'list_triggers.html', token=received_token, chat=access_token.chat)


@config_panel.route('/triggers/', methods=['get', 'post'])
@config_panel.route('/triggers/<trigger_id>', methods=['get', 'post'])
def edit_trigger(trigger_id=None):
    token = request.args.get('token')
    trigger = (create_new_trigger_from_token(token)
        if trigger_id is None
        else Trigger.query.get(trigger_id))

    form = EditTrigger()
    if form.validate_on_submit():
            update_trigger_from_form(trigger, form)
        return redirect_to_list(token)

    joined_answers = '\n'.join([a.text.strip() for a in trigger.answers])
    form = EditTrigger(
        expression=trigger.expression, answers=joined_answers)
    return render_template(
        'edit_trigger.html', form=form, trigger_id=trigger_id, token=token)


@config_panel.route('/triggers/<trigger_id>/delete', methods=['post'])
def delete_trigger(trigger_id):
    token = request.args.get('token')
    access_token = AccessToken.find(token)
    trigger = Trigger.query.get(trigger_id)

    if trigger.chat_id != access_token.chat.chat_id:
        return render_template('invalid_token.html'), 403

    delete_trigger_answers(trigger)
    trigger.delete()
    return redirect_to_list(token)


def redirect_to_list(token):
    list_triggers_url = url_for('config_panel.list_triggers', token=token)
    return redirect(list_triggers_url)


def update_trigger_from_form(current_trigger, form):
    current_trigger.update(expression=form.expression.data.strip())

    delete_trigger_answers(current_trigger)
    for text in form.answers.data.splitlines():
        Answer(text=text, trigger_id=current_trigger.trigger_id).save()


def create_new_trigger_from_token(token):
    access_token = AccessToken.find(token)
    return Trigger(chat_id=access_token.chat.chat_id)


def delete_trigger_answers(trigger):
    for answer in trigger.answers:
        answer.delete()
