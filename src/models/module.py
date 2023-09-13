from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import \
    Enum, Integer, String

from database.db import db


class TMODULE(db.Model):
    __tablename__ = 'T_MODULE'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))
