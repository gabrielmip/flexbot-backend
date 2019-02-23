from flask import Flask, Blueprint
from .models import User

flexbot = Blueprint('flexbot', __name__)

@flexbot.route('/')
def index():
    return 'Hello'