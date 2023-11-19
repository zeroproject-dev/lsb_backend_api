from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Enum, Integer, String

from src.database.db import db


class TROLE(db.Model):
    __tablename__ = "T_ROLE"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    state = Column(Enum("active", "inactive"), server_default=text("'active'"))

    def from_json(self, json):
        self.name = json["name"]
        self.description = (
            json["description"] if json.get("description") is not None else ""
        )
        self.state = "active" if self.state is None else self.state

        return self

    def to_json(self):
        json = {}
        json["id"] = self.id
        json["name"] = self.name
        json["description"] = self.description
        json["state"] = self.state

        return json


class TMODULE(db.Model):
    __tablename__ = "T_MODULE"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    state = Column(Enum("active", "inactive"), server_default=text("'active'"))


class TPERMISSION(db.Model):
    __tablename__ = "T_PERMISSION"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    module_id = Column(Integer, ForeignKey(TMODULE.id))
    state = Column(Enum("active", "inactive"), server_default=text("'active'"))


class TROLEPERMISSION(db.Model):
    __tablename__ = "T_ROLE_PERMISSION"
    id = Column(Integer, primary_key=True)
    permission_id = Column(
        Integer,
    )
    role_id = Column(Integer, ForeignKey(TROLE.id))

    def __init__(self, role, permission) -> None:
        self.permission_id = permission
        self.role_id = role
