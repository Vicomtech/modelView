from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, update
from sqlalchemy.orm import DeclarativeBase
import os



class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

EVAXPLAINIFY_API = f'http://{os.getenv("EVAPI_HOST") or "localhost"}:{os.getenv("EVAPI_PORT") or "8889"}'


class BaseModelMixin (db.Model):
    __abstract__ = True
    
    @classmethod
    def bulk_insert(cls, values:List[Dict[str,any]]):
        stm = insert(cls).returning(cls)
        result = db.session.scalars(stm,values)
        db.session.commit()
        return result.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(cls, id, **values):
        stm = update(cls).where(cls.id == id).values(**values)
        db.session.execute(stm)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def get_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_count(cls, **kwargs):
        return cls.query.distinct().filter_by(**kwargs).count()
    