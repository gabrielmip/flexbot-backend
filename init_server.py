from flask import Flask, url_for
from sqlalchemy.exc import DatabaseError
from flexbot import flexbot
from database import session

app = Flask(__name__)

@app.after_request
def session_commit(response):
    if response.status_code >= 400:
        return response
    try:
        session.commit() # pylint: disable=maybe-no-member
        return response
    except DatabaseError:
        session.rollback() # pylint: disable=maybe-no-member
        raise

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

app.register_blueprint(flexbot, url_prefix='/flexbot')