from sqlalchemy import create_engine, inspect
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

    def to_dict(self):
        return {
            **convert_instance_to_dict(self),
            **convert_relationships_to_dict(self)
        }


def convert_instance_to_dict(instance):
    columns = instance.__table__.columns.keys()
    return {column: getattr(instance, column) for column in columns}


def convert_relationships_to_dict(instance):
    relationship_fields = inspect(instance.__class__).relationships.keys()
    return {
        field: [
            related_entity.to_dict()
            for related_entity in getattr(instance, field)
        ]
        for field in relationship_fields
    }


MyModel = declarative_base(cls=MyBase)
MyModel.query = session.query_property()


def init_db():
    import models
    MyModel.metadata.create_all(bind=engine)
