import datetime
from database import MyModel
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)


class Chat(MyModel):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True)
    title = Column(String(100))
    triggers = relationship('Trigger')


class User(MyModel):
    __tablename__ = 'user'
    user_id = Column('user_id', Integer, primary_key=True)
    first_name = Column(String(100))
    user_name = Column(String(100))


class Message(MyModel):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey(
        Chat.chat_id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey(
        User.user_id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    text = Column(String(400))


class Trigger(MyModel):
    __tablename__ = 'trigger'
    trigger_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey(
        Chat.chat_id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    expression = Column(String(4096))
    answers = relationship("Answer")


class Answer(MyModel):
    __tablename__ = 'answer'
    answer_id = Column(Integer, primary_key=True)
    trigger_id = Column(
        Integer,
        ForeignKey(Trigger.trigger_id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    text = Column(String(4096))


class AccessToken(MyModel):
    __tablename__ = 'access_token'
    token = Column(String(50), primary_key=True)
    chat_id = Column(Integer, ForeignKey(
        Chat.chat_id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    chat = relationship('Chat')

    @staticmethod
    def find(received_token):
        return (AccessToken.query
            .join(AccessToken.chat)
            .filter(AccessToken.token == received_token)
            .first())