from flask import Flask, Blueprint, request, render_template
import logging

from bot.models import Trigger, Answer, Chat, AccessToken
from config import config_panel_url


config_panel = Blueprint('config_panel', __name__, template_folder='templates')


@config_panel.route('/<token>', methods=['get'])
def index(token):
    if token is None:
        return render_template('invalid_token.html')

    access_token = AccessToken.query.filter(AccessToken.token == token).first()
    if access_token is None:
        return render_template('invalid_token.html')

    return render_template('index.html', token=token)
