from flask import Flask
from sqlalchemy.exc import DatabaseError
from database import session
from config import secret_key

# blueprints
from bot import bot
from config_panel import config_panel


app = Flask(__name__, static_folder=None)
app.config['SECRET_KEY'] = secret_key


@app.after_request
def session_commit(response):
    if response.status_code >= 400:
        return response
    try:
        session.commit()  # pylint: disable=maybe-no-member
        return response
    except DatabaseError:
        session.rollback()  # pylint: disable=maybe-no-member
        raise


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


app.register_blueprint(bot, url_prefix='/bot')
app.register_blueprint(config_panel, url_prefix='/config')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
