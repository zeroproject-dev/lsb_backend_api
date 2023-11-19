from dataclasses import dataclass
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Enum, Integer, String, TIMESTAMP, JSON

from src.database.db import db


@dataclass
class TAUDITLOG(db.Model):
    __tablename__ = "T_AUDIT_LOG"

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(255))
    entity_id = Column(Integer)
    action = Column(Enum("insert", "update", "delete"))
    changed_columns = Column(String(255))
    changed_data = Column(JSON)
    timestamp = Column(TIMESTAMP)
    performed_by = Column(Integer)
