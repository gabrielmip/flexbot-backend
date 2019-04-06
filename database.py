from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import datasources


engine = create_engine(datasources['main'])
session = scoped_session(sessionmaker(autocommit=False, bind=engine))


class MyBase(object):

    def save(self):
        session.add(self)  # pylint: disable=maybe-no-member
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)  # pylint: disable=maybe-no-member
        self._flush()

    def _flush(self):
        try:
            session.flush()  # pylint: disable=maybe-no-member
        except DatabaseError:
            session.rollback()  # pylint: disable=maybe-no-member
            raise


MyModel = declarative_base(cls=MyBase)
MyModel.query = session.query_property()


def init_db():
    import bot.models
    MyModel.metadata.create_all(bind=engine)
