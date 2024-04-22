import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Feedbacks(SqlAlchemyBase):
    __tablename__ = 'feedbacks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_email = sqlalchemy.Column(sqlalchemy.String)
