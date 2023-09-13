from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import \
    Enum, Integer, String

from database.db import db
from models.module import TMODULE


class TPERMISSION(db.Model):
    __tablename__ = 'T_PERMISSION'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    module_id = Column(Integer, ForeignKey(TMODULE.id))
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))
