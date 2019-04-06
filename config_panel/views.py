from flask import Blueprint, render_template
from bot.models import AccessToken

config_panel = Blueprint('config_panel', __name__, template_folder='templates')


@config_panel.route('/<received_token>', methods=['get'])
def index(received_token):
    if received_token is None:
        return render_template('invalid_token.html')

    access_token = AccessToken.find(received_token)
    if access_token is None:
        return render_template('invalid_token.html'), 401

    return render_template(
        'index.html', token=received_token, chat=access_token.chat)
