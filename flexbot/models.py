from database import MyModel
from sqlalchemy import (
    Column, Integer, String, MetaData, ForeignKey
)

class Chat(MyModel):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True)
    title = Column(String(100))

class User(MyModel):
    __tablename__ = 'user'
    user_id = Column('user_id', Integer, primary_key=True)
    first_name = Column(String(100))
    user_name = Column(String(100))

class Message(MyModel):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey(Chat.chat_id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    text = Column(String(400))

class Trigger(MyModel):
    __tablename__ = 'trigger'
    trigger_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey(Chat.chat_id), nullable=False)
    expression = Column(String(4096))

class Answer(MyModel):
    __tablename__ = 'answer'
    answer_id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey(Trigger.trigger_id), nullable=False)
    text = Column(String(4096))
