from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import \
    Enum, Integer, String

from database.db import db


class TWORD(db.Model):
    __tablename__ = 'T_WORD'

    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False)
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))
